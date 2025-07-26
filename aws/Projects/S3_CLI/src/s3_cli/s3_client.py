#create a python class for the AWS S3 client
import boto3
from s3_cli.config import Config

class S3Client:
    def __init__(self):
        self.s3_client = boto3.client('s3', region_name=Config.AWS_REGION)

    def list_buckets(self):
        resp = self.s3_client.list_buckets()
        print("Buckets available in s3:")
        for bucket in resp['Buckets']:
            print(f"- {bucket['Name']}")
    
    def list_objects(self, bucket_name):
        resp = self.s3_client.list_objects_v2(Bucket=bucket_name)
        print(f"Objects in bucket '{bucket_name}':")
        print(f"response: {resp}")
        for obj in resp.get('Contents', []):
            print(f"- {obj['Key']}")

    def download_file(self, bucket_name, object_key, local_path):
        print(f"Downloading {object_key} from bucket {bucket_name} to {local_path}...")
        self.s3_client.download_file(bucket_name, object_key, local_path)
        print("Download complete.")

    def upload_file(self, local_path, bucket_name, object_key):
        print(f"Uploading {local_path} to bucket {bucket_name} as {object_key}...")
        self.s3_client.upload_file(local_path, bucket_name, object_key)
        print("Upload complete.")

    def delete_file(self, bucket_name, object_key):
        print(f"Deleting {object_key} from bucket {bucket_name}...")
        self.s3_client.delete_object(Bucket=bucket_name, Key=object_key)
        print("Delete complete.")
    
    def get_object(self, bucket_name, object_key):
        print(f"Getting {object_key} from bucket {bucket_name}...")
        response = self.s3_client.get_object(Bucket=bucket_name, Key=object_key)
        return response['Body'].read()
    
    def put_object(self, bucket_name, object_key, data):
        print(f"Putting object {object_key} in bucket {bucket_name}...")
        self.s3_client.put_object(Bucket=bucket_name, Key=object_key, Body=data)
        print("Put complete.")
    


