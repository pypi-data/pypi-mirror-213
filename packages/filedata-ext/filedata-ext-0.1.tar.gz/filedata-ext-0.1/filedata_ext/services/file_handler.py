import io
import logging
import re
import zipfile
from functools import partial
from hashlib import md5
from typing import List, Optional, Union, Tuple

import gevent
from filedata.file import extract_content_from_file, convert_to_pdf, FileInspection, inspect_file, \
    download_file_from_link
from filedata.image import ocr_result_to_text
from filedata.pdf import pdf_to_image
from filedata.text import normalize_file_content
from flask import current_app
from guniflask.config import settings
from guniflask.utils.context import run_with_context
from kikyo import Kikyo, Search, OSS

from filedata_ext.data_models.file_info import FileInfo, FileContentResult
from filedata_ext.services.filedata_cache import FiledataCacheService
from filedata_ext.utils.video import generate_thumbnail

log = logging.getLogger(__name__)

ALPHA_DIGIT_REG = re.compile(r'^[0-9a-zA-Z]+$')


class FileHandlerService:

    def __init__(self, kikyo_client: Kikyo, filedata_cache: FiledataCacheService):
        self.kikyo_search = kikyo_client.component(cls=Search)
        self.files_bucket = kikyo_client.component(cls=OSS).bucket('files')
        self.filedata_cache = filedata_cache

    def extract_file_content(
            self,
            filename: str = None,
            file_link: str = None,
            file_bytes: bytes = None,
            decompress: bool = False,
            ocr_pdf: bool = None,
    ) -> Union[FileContentResult, Tuple[FileContentResult, Optional[List[FileContentResult]]]]:
        # 根据配置文件判断是否强制开启ocr_pdf
        if ocr_pdf is None:
            try:
                if settings['fd_ocr_pdf']:
                    ocr_pdf = True
                else:
                    ocr_pdf = False
            except Exception:
                ocr_pdf = False

        if file_bytes is None:
            file_bytes = download_file_from_link(file_link).content

        _md5 = md5(file_bytes).hexdigest()

        file_info = self.filedata_cache.get_file_info_cache(_md5)
        if file_info is None:
            file_info = FileInfo(md5=_md5)

        try:
            meta = inspect_file(file_bytes, timeout=60)
        except Exception:
            _filename = filename or ''
            _s = _filename.rsplit('.', maxsplit=1)
            if len(_s) > 1 and ALPHA_DIGIT_REG.match(_s[-1]):
                _file_ext = _s[-1]
            else:
                _file_ext = None
            meta = FileInspection(
                file_bytes=file_bytes,
                file_ext=_file_ext,
            )

        # 处理zip
        if decompress and meta.content_type == 'application/zip':
            _zip_result = self._handle_files_in_zip(file_bytes)
        else:
            _zip_result = None

        content = ''
        file_snapshots = []
        if meta.content_type is not None and meta.content_type.startswith('image/'):
            try:
                if file_info.content and file_info.snapshots:
                    content = file_info.content
                    file_snapshots = file_info.snapshots
                else:
                    ocr_cache = self.filedata_cache.ocr_image(
                        md5=_md5,
                        file_bytes=file_bytes,
                        filename=filename,
                        file_link=file_link,
                    )
                    content = ocr_result_to_text(ocr_cache.ocr_result[0])
                    file_snapshots = [ocr_cache.meta[0].file_link]
            except Exception:
                pass
        else:
            if meta.content_type is not None and meta.content_type.startswith('audio/'):
                pass
            elif meta.content_type is not None and meta.content_type.startswith('video/'):
                try:
                    file_snapshots = self._get_video_thumbnail(file_link or file_bytes, _md5)
                except Exception as e:
                    current_app.logger.warning(f'Failed to get video snapshot: {e}', exc_info=True)
            else:
                try:
                    if file_info.content:
                        content = file_info.content
                    else:
                        content = extract_content_from_file(meta.file_bytes, timeout=60)

                    if file_info.snapshots:
                        file_snapshots = file_info.snapshots
                    else:
                        if meta.file_ext == 'pdf':
                            pdf = meta.file_bytes
                        else:
                            pdf = convert_to_pdf(meta.file_bytes, filename=filename, timeout=60)
                        if pdf:
                            if ocr_pdf:
                                # 对pdf进行ocr
                                ocr_cache = self.filedata_cache.ocr_pdf(
                                    md5=_md5,
                                    file_bytes=pdf,
                                    filename=filename,
                                    file_link=file_link,
                                )
                                for m in ocr_cache.meta:
                                    file_snapshots.append(m.file_link)
                            else:
                                img_list = pdf_to_image(pdf, limit=self.filedata_cache.thumbnail_num)
                                for i, r in enumerate(img_list):
                                    key = f'snapshots/{_md5}_{i}.jpeg'
                                    self.files_bucket.put_object(key, img_list[i])
                                    link = self.files_bucket.get_object_link(key)
                                    file_snapshots.append(link)
                except Exception:
                    pass

        if content:
            content = normalize_file_content(content)

        # 更新global file
        cache_updated = False
        if not file_info.content:
            file_info.content = content
            cache_updated = True
        if not file_info.snapshots:
            file_info.snapshots = file_snapshots
            cache_updated = True
        if cache_updated:
            self.filedata_cache.save_file_info_cache(md5=_md5, file_info_cache=file_info)

        result = FileContentResult(
            meta=meta,
            content=content,
            snapshots=file_snapshots,
            filename=filename,
            size=len(file_bytes),
        )
        if decompress:
            return result, _zip_result
        return result

    def _decompress_zip_file(self, file_bytes) -> List[dict]:
        result = []
        fio = io.BytesIO(file_bytes)
        zip_file = zipfile.ZipFile(fio)
        for info in zip_file.infolist():
            if info.file_size > 0:
                try:
                    filename = recode_zip_filename(info.filename)
                    b = zip_file.read(info.filename)
                except Exception as e:
                    current_app.logger.warning(f'Error occurred when decompress zip file: {e}', exc_info=True)
                else:
                    result.append({
                        'filename': filename,
                        'file_bytes': b
                    })
        return result

    def _handle_files_in_zip(self, file_bytes) -> List[FileContentResult]:
        _files = self._decompress_zip_file(file_bytes)
        jobs = []
        for _file in _files:
            jobs.append(
                gevent.spawn(
                    run_with_context(
                        partial(self.extract_file_content, filename=_file['filename'], file_bytes=_file['file_bytes'])
                    )
                )
            )
        gevent.wait(jobs)
        result = []
        for job in jobs:
            try:
                v = job.get()
                assert isinstance(v, FileContentResult)
                result.append(v)
            except Exception:
                pass
        return result

    def _get_video_thumbnail(self, video_link: Union[str, bytes], file_md5: str) -> List[str]:
        img_bytes = generate_thumbnail(video_link)
        file_snapshots = []
        if img_bytes:
            key = f'snapshots/{file_md5}_0.jpg'
            self.files_bucket.put_object(key, img_bytes)
            file_snapshots.append(self.files_bucket.get_object_link(key))
        return file_snapshots


def recode_zip_filename(s: str) -> str:
    try:
        return s.encode('cp437').decode('gbk')
    except Exception:
        return s.encode('cp437').decode('utf-8')
