from typing import List

from filedata.image import RegionBox
from pydantic import BaseModel, Field


class DocFeature(BaseModel):
    secret_mark: str = Field(default=None, title='国家秘密标志')
    secret_mark_position: RegionBox = Field(default=None, title='国家秘密标志位置')
    secret_mark_crop: str = Field(default=None, title='国家秘密标志截图')
    title: str = Field(default=None, title='公文标题')
    title_position: RegionBox = Field(default=None, title='公文标题位置')
    title_crop: str = Field(default=None, title='公文标题截图')
    number: str = Field(default=None, title='公文字号')
    number_position: RegionBox = Field(default=None, title='公文字号位置')
    number_crop: str = Field(default=None, title='公文字号截图')
    sender: List[str] = Field(default=None, title='发文单位')
    sender_position: List[RegionBox] = Field(default=None, title='发文单位位置')
    sender_crop: List[str] = Field(default=None, title='发文单位截图')
    sender_seal: List[str] = Field(default=None, title='发文单位公章')
    sender_seal_position: List[RegionBox] = Field(default=None, title='发文单位公章位置')
    sender_seal_crop: List[str] = Field(default=None, title='发文单位公章截图')
    secret_annotation: str = Field(default=None, title='工作秘密标志')
    secret_annotation_position: RegionBox = Field(default=None, title='工作秘密标志位置')
    secret_annotation_crop: str = Field(default=None, title='工作秘密标志截图')
