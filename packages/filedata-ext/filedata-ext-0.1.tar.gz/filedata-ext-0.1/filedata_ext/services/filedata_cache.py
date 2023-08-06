import io
from typing import List, Optional, Any

import gevent
import requests
from PIL import Image
from filedata.image import ocr_with_angle_correction, OCRResult
from filedata.pdf import pdf_to_image
from filedata.retry import retry_api
from guniflask.config import settings
from kikyo import Kikyo, OSS
from kikyo.bundle.search import EsBasedSearch
from pydantic import BaseModel

from filedata_ext.constants import FILEDATA_CACHE_ENDPOINT, THUMBNAIL_NUM
from filedata_ext.data_models.doc_feature import DocFeature
from filedata_ext.data_models.file_info import FileInfo
from filedata_ext.data_models.ocr import OCRCache, OCRMeta


class Cache(BaseModel):
    filename: str = None
    md5: str
    file_link: str = None
    data: Any


class CacheKey:
    OCR = 'ocr'
    FEATURES = 'features'
    HIT_INFO = 'hit_info'
    FILE_INFO = 'file_info'


class FiledataCacheService:
    def __init__(self, kikyo_client: Kikyo):
        self.kikyo_search = kikyo_client.component(cls=EsBasedSearch)
        self.files_bucket = kikyo_client.component(cls=OSS).bucket('files')

        self.session = requests.Session()
        try:
            self.endpoint = settings['fd_filedata_cache_endpoint'] or FILEDATA_CACHE_ENDPOINT
        except Exception:
            self.endpoint = FILEDATA_CACHE_ENDPOINT
        try:
            self.thumbnail_num = settings['fd_thumbnail_num'] or THUMBNAIL_NUM
        except Exception:
            self.thumbnail_num = THUMBNAIL_NUM

    def ocr_image(
            self,
            md5: str,
            file_bytes: bytes,
            filename: str = None,
            file_link: str = None,
    ) -> OCRCache:
        ocr_cache = self.get_ocr_cache(md5)
        if ocr_cache:
            return ocr_cache

        ocr_result = ocr_with_angle_correction(file_bytes, timeout=60)
        key = f'snapshots/{md5}.jpeg'
        self.files_bucket.put_object(key, ocr_result.img)
        _img_link = self.files_bucket.get_object_link(key)
        _img: Image.Image = Image.open(io.BytesIO(ocr_result.img))
        ocr_cache = OCRCache(
            filename=filename,
            md5=md5,
            meta=[OCRMeta(
                file_link=_img_link,
                width=_img.width,
                height=_img.height,
            )],
            ocr_result=[ocr_result.ocr_regions],
            file_link=file_link,
        )

        self.save_ocr_cache(ocr_cache)
        return ocr_cache

    def ocr_pdf(
            self,
            md5: str,
            file_bytes: bytes,
            filename: str = None,
            file_link: str = None,
    ) -> OCRCache:
        """
        需要提供原始文件的md5
        """
        ocr_cache = self.get_ocr_cache(md5)
        if ocr_cache:
            return ocr_cache

        meta = []
        ocr_result = []
        img_list = pdf_to_image(file_bytes, limit=self.thumbnail_num)

        result_list = self._do_ocr(img_list)
        for i, r in enumerate(result_list):
            key = f'snapshots/{md5}_{i}.jpeg'
            self.files_bucket.put_object(key, r.img)
            link = self.files_bucket.get_object_link(key)
            _img: Image.Image = Image.open(io.BytesIO(r.img))
            meta.append(
                OCRMeta(
                    file_link=link,
                    width=_img.width,
                    height=_img.height,
                )
            )
            ocr_result.append(r.ocr_regions)

        ocr_cache = OCRCache(
            filename=filename,
            md5=md5,
            meta=meta,
            ocr_result=ocr_result,
            file_link=file_link,
        )
        self.save_ocr_cache(ocr_cache)
        return ocr_cache

    def _do_ocr(self, img_list: List[bytes]) -> List[OCRResult]:
        jobs = []
        for img in img_list:
            jobs.append(
                gevent.spawn(ocr_with_angle_correction, img, timeout=60)
            )
        gevent.wait(jobs)
        result = []
        for j in jobs:
            result.append(j.get())
        return result

    def get_ocr_cache(self, md5: str) -> Optional[OCRCache]:
        cache = self.get_cache(key=CacheKey.OCR, md5=md5)
        if cache is None:
            return
        return OCRCache(**cache.data)

    def save_ocr_cache(self, ocr_cache: OCRCache):
        self.save_cache(key=CacheKey.OCR, cache=Cache(md5=ocr_cache.md5, data=ocr_cache))

    def get_features_cache(self, md5: str) -> Optional[List[DocFeature]]:
        cache = self.get_cache(key=CacheKey.FEATURES, md5=md5)
        if cache is None:
            return
        result = [DocFeature(**i) for i in cache.data]
        return result

    def save_features_cache(self, md5: str, features: List[DocFeature]):
        self.save_cache(key=CacheKey.FEATURES, cache=Cache(md5=md5, data=features))

    def get_file_info_cache(self, md5: str) -> Optional[FileInfo]:
        cache = self.get_cache(key=CacheKey.FILE_INFO, md5=md5)
        if cache is None:
            return
        return FileInfo(**cache.data)

    def save_file_info_cache(self, md5: str, file_info_cache: FileInfo):
        self.save_cache(key=CacheKey.FILE_INFO, cache=Cache(md5=md5, data=file_info_cache))

    @retry_api
    def get_cache(self, key: str, md5: str) -> Optional[Cache]:
        resp = self.session.get(
            f'{self.endpoint}api/cache',
            params={
                'md5': md5,
                'key': key,
            },
            timeout=20,
        )
        if resp.status_code == 404:
            return
        resp.raise_for_status()
        return Cache(**resp.json()['data'])

    def save_cache(self, key: str, cache: Cache):
        self.session.post(
            f'{self.endpoint}api/cache',
            json=cache.dict(),
            params={
                'key': key,
            },
            timeout=20,
        )
