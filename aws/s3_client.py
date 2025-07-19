import boto3

s3_client = boto3.client('s3')


resp=s3_client.list_buckets()
print("Available buckets:")
for bucket in resp['Buckets']:
    print(f"- {bucket['Name']}")


print(f"Downloading image from S3 bucket...")
s3_client.download_file('mvawsbucket-1', 'wallpaper.jpg', './local_image.jpg')