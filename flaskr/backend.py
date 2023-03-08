from google.cloud import storage
import hashlib
class Backend:

    def __init__(self, bucket_name):
        self.bucket_name = bucket_name
        self.client = storage.Client()
        self.bucket = self.client.bucket(bucket_name)
        
    def get_wiki_page(self, name):
        pass

    def get_all_page_names(self):
        page_names = self.bucket.list_blobs()
        return [f.name for f in page_names]

    def upload(self, file_path):
        blob = self.bucket.blob(file_path)
        blob.upload_from_filename(file_path)

    def sign_up(self,username,password):
        # user_bucket = self.storage_client.bucket(self.user_bucket_name)
        prefix_for_password = 'tech_exchange'
        prefixed_password = prefix_for_password + password
        hashed_password = hashlib.sha256(prefixed_password.encode()).hexdigest()
        blob = self.bucket.blob(username)
        if blob.exists():
            return False
        else:
            blob.upload_from_string(hashed_password)
            return True

    def sign_in(self,username,password):
        prefix_for_password = 'tech_exchange'
        prefixed_password = prefix_for_password + password
        hashed_password = hashlib.sha256(prefixed_password.encode()).hexdigest()
        blob = self.bucket.blob(username)
        bucket_password = blob.download_as_string().decode('utf-8')
        if blob.exists():
            if hashed_password == bucket_password:
                return True
        else:
            return False
        

    def get_image(self, image_name):
        """Gets an image from the image bucket."""
        blob = self.bucket.blob(image_name)
        if blob.exists():
            return blob.public_url
        else:
            return None