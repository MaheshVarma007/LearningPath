
from s3_cli.app import App


if __name__ == "__main__":
    print("Starting S3 CLI application...")
    app = App()
    app.run()
    print("S3 CLI application finished running.")