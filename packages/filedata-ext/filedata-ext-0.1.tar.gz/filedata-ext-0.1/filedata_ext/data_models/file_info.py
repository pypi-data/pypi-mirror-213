from typing import List

from filedata.file import FileInspection
from pydantic import BaseModel


class FileInfo(BaseModel):
    filename: str = None
    md5: str = None
    content: str = None
    snapshots: List[str] = None


class FileContentResult(BaseModel):
    meta: FileInspection
    content: str
    snapshots: List[str]
    filename: str = None
    size: int = None
