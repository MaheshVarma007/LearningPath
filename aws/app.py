from s3_client import S3Client


def app():
    print("AWS S3 Client Application")
    s3_client = S3Client()
    
    # List all buckets
    s3_client.list_buckets()
    
    # List objects in a specific bucket
    s3_client.list_objects('mvawsbucket-1')
    
    # Download a file from S3
    s3_client.download_file('mvawsbucket-1', 'sample.png', './downloaded_sample.png')
    
    # Upload a file to S3
    s3_client.upload_file('./sample.png', 'mvawsbucket-1', 'local_image.jpg')
    
    # Delete a file from S3
    s3_client.delete_file('mvawsbucket-1', 'local_image.jpg')
    
    # Get an object from S3
    content = s3_client.get_object('mvawsbucket-1', 'dummy.txt')
    print(content.decode('utf-8'))


if __name__ == "__main__":
    app()
