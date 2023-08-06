from typing import List

from filedata.image import OCRRegion
from pydantic import BaseModel


class OCRMeta(BaseModel):
    file_link: str = None
    width: int = None
    height: int = None


class OCRCache(BaseModel):
    filename: str = None
    md5: str = None
    meta: List[OCRMeta] = None
    ocr_result: List[List[OCRRegion]] = None
    file_link: str = None
