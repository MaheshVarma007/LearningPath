# Base image
FROM python:3.12-slim

# Set work directory
WORKDIR /S3_CLI/src

# Copy dependencies and install
COPY requirements.txt /S3_CLI/
RUN pip install --no-cache-dir -r /S3_CLI/requirements.txt

# Copy the source code
COPY src/ /S3_CLI/src/

# Set entrypoint
ENTRYPOINT ["python", "-m", "s3_cli.__main__"]
