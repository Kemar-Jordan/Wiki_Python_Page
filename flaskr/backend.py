# Imports the Google Cloud client library
from google.cloud import storage

# TODO(Project 1): Implement Backend according to the requirements.
class Backend:

    def __init__(self,bucket_name):
        self.bucket = storage.Client().bucket(bucket_name)     

    def get_wiki_page(self, name):
        pass

    def get_all_page_names(self):
        pass

    def upload(self):
        pass

    def sign_up(self):
        pass

    def sign_in(self):
        pass

    def get_image(self, image_name):
        """Gets an image from the image bucket."""
        blob = self.bucket.blob(image_name)
        if blob.exists():
            return blob.download_as_bytes()
        else:
            return None