from s3_cli.config import Config
from s3_cli.s3_manager import S3Manager
import argparse
import os

#CLI Tool for AWS S3 operations
#This tool allows users to perform various S3 operations like upload, download, delete, etc
class App:
    def __init__(self):
        self.s3_manager = S3Manager()

    def run(self):
        parser = argparse.ArgumentParser(description="MY AWS S3 CLI")
        sub=parser.add_subparsers(dest='command', help='Available commands', required=True)

        # Define subcommands
        upload_cmd = sub.add_parser("upload", help="Upload file")
        upload_cmd.add_argument("local_path", help="Local file path to upload")
        upload_cmd.add_argument("object_key", help="S3 object key")

        download_cmd = sub.add_parser("download", help="Download file")
        download_cmd.add_argument("object_key", help="S3 object key to download")   
        download_cmd.add_argument("local_path", help="Local path to save the downloaded file")

        delete_cmd = sub.add_parser("delete", help="Delete file")
        delete_cmd.add_argument("object_key", help="S3 object key to delete")

        get_object_cmd = sub.add_parser("get_object", help="Get object data")
        get_object_cmd.add_argument("object_key", help="S3 object key to get data from")
        get_object_cmd.add_argument("local_path", help="Local path to save the object data")

        put_object_cmd = sub.add_parser("put_object", help="Put object data")
        put_object_cmd.add_argument("object_key", help="S3 object key to put data into")
        put_object_cmd.add_argument("data", help="Data to put into the S3 object")

        list_objects_cmd = sub.add_parser("list_objects", help="List objects in bucket")
        list_objects_cmd.add_argument("prefix", help="Prefix to filter objects")

        list_buckets_cmd = sub.add_parser("list_buckets", help="List all S3 buckets")


        #sub.add_parser('list_buckets', help='List all S3 buckets')

        
        args = parser.parse_args()

        if args.command == "list_buckets":
            self.s3_manager.list_buckets()

        elif args.command == "list_objects":
            self.s3_manager.list_objects()

        elif args.command == "download":
            self.s3_manager.download_file(args.object_key, args.local_path)

        elif args.command == "upload":
            self.s3_manager.upload_file(args.local_path, args.object_key)

        elif args.command == "delete":
            self.s3_manager.delete_file(args.object_key)

        elif args.command == "get_object":
            data = self.s3_manager.get_object(args.object_key)
            with open(args.local_path, 'wb') as f:
                f.write(data)
            print(f"Data from {args.object_key} saved to {args.local_path}")
        
        elif args.command == "put_object":
            self.s3_manager.put_object(args.object_key, args.data)
            print(f"Data put into {args.object_key}")

        else:
            parser.print_help()
            exit(1)
        