from s3_cli.config import Config
from s3_cli.s3_client import S3Client

class S3Manager:
    def __init__(self):
        self.s3_client = S3Client()

    def list_buckets(self):
        self.s3_client.list_buckets()

    def list_objects(self):
        self.s3_client.list_objects(Config.BUCKET_NAME)

    def download_file(self, object_key, local_path):
        self.s3_client.download_file(Config.BUCKET_NAME, object_key, local_path)

    def upload_file(self, local_path, object_key):
        self.s3_client.upload_file(local_path, Config.BUCKET_NAME, object_key)

    def delete_file(self, object_key):
        self.s3_client.delete_file(Config.BUCKET_NAME, object_key)

    def get_object(self, object_key):
        return self.s3_client.get_object(Config.BUCKET_NAME, object_key)

    def put_object(self, object_key, data):
        self.s3_client.put_object(Config.BUCKET_NAME, object_key, data)