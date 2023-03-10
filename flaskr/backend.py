from google.cloud import storage
import hashlib

storage_client = storage.Client()

class Backend:
    '''
    Provides an interface for the underlying GCS buckets
    '''
    def __init__(self, bucket_name):
        self.bucket_name = bucket_name
        self.client = storage.Client()
        self.bucket = self.client.bucket(bucket_name)
        
    def get_wiki_page(self, name):
        '''
        Gets an uploaded page from the content bucket.
        '''
        pass

    def get_all_page_names(self):
        '''
        Gets the names of all pages from the content bucket.
        '''
        blob = self.bucket.blob(f"wiki-user-uploads")
        page_names = self.bucket.list_blobs()
        return [f.name for f in page_names]

    def upload(self,filepath,filename):
        '''
        Adds data to the content bucket.
        '''
        blob = self.bucket.blob(f"wiki-user-uploads/{filename}")
        blob.upload_from_filename(filepath, content_type="text.html")
        
    def sign_up(self,username,password):
        '''
        Adds user data if it does not exist along with a hashed password.
        '''
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
        '''
        Checks if a password, when it hashed, matches the password in the user bucket.
        '''
        prefix_for_password = 'tech_exchange'
        prefixed_password = prefix_for_password + password
        hashed_password = hashlib.sha256(prefixed_password.encode()).hexdigest()
        blob = self.bucket.blob(username)
        bucket_password = blob.download_as_bytes().decode('utf-8')
        if blob.exists():
            if hashed_password == bucket_password:
                return True
        else:
            return False

    def get_image(self, image_name):
        '''
        Gets an image from the content bucket.
        '''
        blob = self.bucket.blob(image_name)
        if blob.exists():
            return blob.public_url
        else:
            return None