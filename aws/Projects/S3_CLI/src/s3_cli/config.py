import os

class Config:
    AWS_REGION = os.getenv("AWS_REGION", "ap-southeast-1")
    BUCKET_NAME = os.getenv("BUCKET_NAME", "mvawsbucket-1")
