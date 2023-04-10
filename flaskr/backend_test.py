import unittest
from unittest.mock import MagicMock, patch
from google.cloud import storage
from flaskr.backend import Backend
import hashlib

class TestBackend(unittest.TestCase):

    @patch.object(storage, 'Client')
    def setUp(self, mock_client):
        '''
        Set up method defines mock client, bucket and storage before and after each test method
        '''
        # Mock the storage.Client class and create a Backend instance
        self.mock_client = mock_client
        self.mock_bucket = mock_client.return_value.bucket.return_value
        self.backend = Backend('test-bucket')

    @patch.object(storage, 'Client')
    def test_init(storage, mock_client):
        '''
        Test for init method
        '''
        # Create backend instance and test attributes
        backend = Backend('test-bucket')
        assert backend.bucket_name == 'test-bucket'
        mock_client.assert_called_once()
        mock_client.return_value.bucket.assert_called_once_with('test-bucket')

    @patch.object(storage, 'Client')
    def test_sign_up(self, mock_client):
        '''
        Test for sign up method
        '''
        # Mock bucket object, blob and client and attributes within them
        mock_bucket = MagicMock()
        mock_blob = MagicMock()
        mock_blob.exists.return_value = False
        mock_bucket.blob.return_value = mock_blob
        mock_client.return_value.bucket.return_value = mock_bucket

        # Create Backend instance and call the sign_up method
        backend = Backend('test-bucket')
        result = backend.sign_up('test-user', 'test-password')
        
        # Assert called once will test various methods during the sign up
        mock_client.return_value.bucket.assert_called_once_with('test-bucket')
        mock_bucket.blob.assert_called_once_with('test-user')
        mock_blob.exists.assert_called_once()
        self.assertTrue(result)

    def test_sign_in_success(self):
        '''
        Test for successful sign-in
        '''
        username = 'test-user'
        password = 'test-password'
        prefixed_password = 'tech_exchange' + password
        hashed_password = hashlib.sha256(prefixed_password.encode()).hexdigest()
        self.mock_bucket.blob.return_value.download_as_bytes.return_value = hashed_password.encode()
        result = self.backend.sign_in(username, password)
        self.assertTrue(result)

    def test_sign_in_unknown(self):
        '''
        Test for non-existent user
        '''
        username = 'unknown-user'
        password = 'test-password'
        result = self.backend.sign_in(username, password)
        self.assertFalse(result)

    @patch.object(storage.blob.Blob, 'upload_from_filename')
    def test_upload_success(self, mock_upload):
        '''
        Test for successful upload
        '''
        filepath = 'test-file.html'
        filename = 'test-file.html'
        username = 'test-user'
        mock_blob = MagicMock()
        mock_blob.name = f"wiki-user-uploads/{username}/{filename}"
        self.mock_bucket.blob.return_value = mock_blob
        self.backend.upload(filepath, filename, username)
        mock_blob.upload_from_filename.assert_called_once_with(filepath, content_type="text.html")
        self.assertEqual(mock_blob.name, f"wiki-user-uploads/{username}/{filename}")

    def test_upload_fail(self):
        '''
        Test for failed upload
        '''
        filepath = 'test-file.html'
        filename = 'test-file.html'
        expected_exception = Exception('Error uploading file')
        self.mock_bucket.blob.side_effect = expected_exception
        with self.assertRaises(Exception) as context:
            self.backend.upload(filepath, filename, 'test-user')
        self.assertEqual(str(context.exception), str(expected_exception))

class TestBackend2(unittest.TestCase):

    @patch('google.cloud.storage.Client')
    def setUp(self, mock_storage_client):
        '''
        Set up method defines mock bucket for backend before and after each test method
        '''
        self.bucket_name = 'test-bucket'
        self.backend = Backend(self.bucket_name)

    def test_get_image_success(self):
        '''
        Test for successfully getting an image
        '''
        image_name = 'test-image.jpg'
        blob_mock = MagicMock()
        blob_mock.exists.return_value = True
        blob_mock.public_url = 'https://storage.googleapis.com/test-bucket/test-image.jpg'
        self.backend.bucket.blob.return_value = blob_mock
        result = self.backend.get_image(image_name)
        self.assertEqual(result, 'https://storage.googleapis.com/test-bucket/test-image.jpg')

    def test_get_image_fail(self):
        '''
        Test for failing to get an image
        '''
        image_name = 'non-existent-image.jpg'
        blob_mock = MagicMock()
        blob_mock.exists.return_value = False
        self.backend.bucket.blob.return_value = blob_mock
        result = self.backend.get_image(image_name)
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()