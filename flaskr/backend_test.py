from flaskr.backend import Backend
from google.cloud import storage
import pytest

# TODO(Project 1): Write tests for Backend methods.
@pytest.fixture
def backend():
    return Backend('wiki-backend-test-bucket')

def test_init(backend):
    assert backend.bucket_name == 'wiki-backend-test-bucket'
    assert isinstance(backend.client, storage.Client)
    assert isinstance(backend.bucket, storage.Bucket)