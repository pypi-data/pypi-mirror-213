from os.path import dirname, join

import pytest
from kikyo import configure_by_consul

from filedata_ext.data_models.file_info import FileContentResult
from filedata_ext.services.file_handler import FileHandlerService
from filedata_ext.services.filedata_cache import FiledataCacheService


@pytest.fixture(scope='module')
def kikyo_client():
    return configure_by_consul('http://consul.app.kdsec.org/v1/kv/kikyo')


@pytest.fixture(scope='module')
def filedata_cache(kikyo_client):
    return FiledataCacheService(kikyo_client=kikyo_client)


@pytest.fixture(scope='module')
def file_handler(kikyo_client, filedata_cache):
    return FileHandlerService(kikyo_client=kikyo_client, filedata_cache=filedata_cache)


resource_dir = join(dirname(__name__), 'resources')


def test_image(file_handler: FileHandlerService):
    with open(join(resource_dir, 'example.png'), 'rb') as f:
        img_bytes = f.read()
    result = file_handler.extract_file_content(file_bytes=img_bytes)
    assert isinstance(result, FileContentResult)
    assert '舒城县人民政府文件' in result.content


def test_office_doc(file_handler: FileHandlerService):
    with open(join(resource_dir, 'example.docx'), 'rb') as f:
        file_bytes = f.read()
    result = file_handler.extract_file_content(file_bytes=file_bytes)
    assert isinstance(result, FileContentResult)
    assert '行政规范性文件认定标准' in result.content


def test_pdf(file_handler: FileHandlerService):
    with open(join(resource_dir, 'example.pdf'), 'rb') as f:
        file_bytes = f.read()
    result = file_handler.extract_file_content(file_bytes=file_bytes)
    assert isinstance(result, FileContentResult)
    assert '党政机关公文处理工作条例' in result.content
