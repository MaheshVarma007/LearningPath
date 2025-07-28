# Docker Setup & Usage

## 1. Prepare your `.env` file

Create a `.env` file in the project root (same directory as the Dockerfile) with the following format (no quotes):

```
AWS_ACCESS_KEY_ID=your-access-key-id
AWS_SECRET_ACCESS_KEY=your-secret-access-key
AWS_DEFAULT_REGION=ap-southeast-1
```

## 2. Build the Docker image

Run this command in the directory containing the Dockerfile:

```sh
docker build -t s3_cli_app .
```

## 3. Run the CLI using Docker

To run the CLI and pass AWS credentials from your `.env` file:

```sh
docker run --rm --env-file .env s3_cli_app <command>
```

Replace `<command>` with your desired CLI command, e.g.:

```sh
docker run --rm --env-file .env s3_cli_app list_buckets
```

## Notes
- Ensure your `.env` file does not have quotes around the values.
- The `.env` file must be in the same directory where you run the `docker run` command, or provide the correct path.

# S3 CLI Application

## Overview

The S3 CLI Application is a command-line tool designed to interact with Amazon S3 buckets. It provides a user-friendly interface for performing common S3 operations such as uploading, downloading, listing, and deleting files. The application is built in Python and is structured for easy extension and maintenance.

---

## Features

- **Upload files to S3 buckets**
- **Download files from S3 buckets**
- **List files and folders in a bucket**
- **Delete files from S3 buckets**
- **Configurable AWS credentials and region**
- **Extensible architecture for adding new commands**

---

## Getting Started

### Prerequisites
- Python 3.7+
- AWS account and S3 access
- AWS credentials configured (via environment variables, AWS CLI, or config file)

### Installation

1. Clone the repository:
   ```sh
   git clone <your-repo-url>
   cd S3_CLI
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

---

## Usage

Run the CLI application from the command line:

```sh
python -m s3_cli
```

Or, if you want to run the main entry point directly:

```sh
python src/s3_cli/__main__.py
```

You will see:
```
Starting S3 CLI application...
... (application output) ...
S3 CLI application finished running.
```

---

## Configuration

The application uses AWS credentials from your environment. You can set them up using the AWS CLI:

```sh
aws configure
```

Or set the following environment variables:
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_DEFAULT_REGION`

---

## Project Structure

```
S3_CLI/
├── src/
│   └── s3_cli/
│       ├── __main__.py      # Main entry point
│       ├── app.py           # Application logic
│       └── ...              # Other modules
├── requirements.txt         # Python dependencies
├── README.md                # Documentation
└── ...
```

---

## Extending the Application

To add new commands or features:
1. Create a new module in `src/s3_cli/`.
2. Register your command in `app.py`.
3. Update the documentation as needed.

---

## Developer Notes

- The code is modular and follows best practices for maintainability.
- Logging and error handling are included for easier debugging.
- Contributions are welcome! Please submit pull requests with clear descriptions.

---

## Troubleshooting

- **AWS Credentials Error:** Ensure your credentials are set up correctly.
- **Module Not Found:** Check your Python path and installation.
- **Permission Issues:** Make sure your IAM user has the necessary S3 permissions.

---

## License

This project is licensed under the MIT License.

---

## Contact

For questions or support, please open an issue on GitHub or contact the maintainer.
