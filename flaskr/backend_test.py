from flaskr.backend import Backend
from google.cloud import storage
from unittest.mock import MagicMock, patch
import hashlib
import pytest
import tempfile

@pytest.fixture
def backend():
    return Backend('wiki-backend-test-bucket')

# Testing __init__ method
def test_init(backend):
    assert backend.bucket_name == 'wiki-backend-test-bucket'
    assert isinstance(backend.client, storage.Client)
    assert isinstance(backend.bucket, storage.Bucket)

# Testing get_wiki_page method
def test_get_wiki_page(backend):
    # Create mock objects for storage client and blob
    storage_client = MagicMock()
    blob = MagicMock()
    # Expected returned url 
    blob.public_url = 'https://storage.googleapis.com/wiki-user-uploads/wiki-user-uploads/test-file'
    with patch('google.cloud.storage.Client', return_value = storage_client):
        url = backend.get_wiki_page('test-file')
        assert url == blob.public_url

# Test #1 for sign_up, testing the sign up of a new user with a valid username and password, should return True
def test_sign_up_1(backend):
    username = 'new_valid_user'
    password = 'new_valid_password'
    assert backend.sign_up(username, password) == True
    # Delete user after testing the sign up
    assert backend.delete_user(username) == True

# Test #2 for sign_up method, testing the sign up of existing users, the method should return False
def test_sign_up_2(backend):
    username = 'existing_user'
    password = 'existing_password'
    blob = backend.bucket.blob(username)
    blob.upload_from_string('existing_password_hash')
    assert backend.sign_up(username, password) == False

# Test #3 sign_up method, testing if a password is correctly hashed
def test_sign_up_3(backend):
    username = 'new_user'
    password = 'new_password'
    backend.sign_up(username, password)
    blob = backend.bucket.blob(username)
    bucket_password_hash = blob.download_as_bytes().decode('utf-8')
    prefix_for_password = 'tech_exchange'
    prefixed_password = prefix_for_password + password
    expected_hashed_password = hashlib.sha256(prefixed_password.encode()).hexdigest()
    assert bucket_password_hash == expected_hashed_password

# Test #1 get_image method, testing if we are returned the correct URL for an image
def test_get_image_1(backend):
    image_name = 'test_image.jpg'
    mock_blob = MagicMock()
    mock_blob.exists.return_value = True
    mock_blob.public_url = 'https://storage.googleapis.com/wiki-backend-test-bucket/test_image.jpg'
    with patch.object(backend.bucket, 'blob', return_value = mock_blob):
        result = backend.get_image(image_name)
    assert result == 'https://storage.googleapis.com/wiki-backend-test-bucket/test_image.jpg'

# Test #2 get_image method, we pass through a jpg that doesn't exist and expect to be return None
def test_get_image_2(backend):
    image = 'mock_nonexistent.jpg'
    mock_blob = MagicMock()
    mock_blob.exists.return_value = False
    with patch.object(backend.bucket, 'blob', return_value = mock_blob):
        result = backend.get_image(image)
    assert result is None

# Test #1 the upload method, this tests a situation where the upload is a success
def test_upload_1(backend):
    with tempfile.NamedTemporaryFile(delete = False) as temp_file:
        temp_file.write(b"test data")
        temp_file.flush()
        temp_file_name = temp_file.name.split("/")[-1]
        backend.upload(temp_file.name, temp_file_name)
        blob = backend.bucket.blob(f"wiki-user-uploads/{temp_file_name}")
        assert blob.exists()

# Testing the upload method, this tests a situation where the upload is a failure
def test_upload_2(backend):
    with pytest.raises(FileNotFoundError):
        backend.upload("invalid_file_path", "invalid_file_name")