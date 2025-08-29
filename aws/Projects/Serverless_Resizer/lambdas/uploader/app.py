import json, os, time, uuid, boto3

s3 = boto3.client("s3")
BUCKET = os.environ.get("BUCKET", "img-resizer-dev-ee03ffe6")

def _response(status, body):
    return {
        "statusCode": status,
        "headers": {"content-type": "application/json"},
        "body": json.dumps(body)
    }

def handler(event, context):
    try:
        body = json.loads(event.get("body") or "{}")
        print(f"body: {body}")
        filename = body.get("filename") or f"{uuid.uuid4()}.jpg"
        print(f"filename: {filename}")
        content_type = body.get("contentType", "image/jpeg")
        key = f"originals/{int(time.time())}-{filename}"

        url = s3.generate_presigned_url(
            ClientMethod="put_object",
            Params={"Bucket": BUCKET, "Key": key, "ContentType": content_type},
            ExpiresIn=300,  # 5 minutes
            HttpMethod="PUT",
        )
        return _response(200, {"uploadUrl": url, "key": key})
    except Exception as e:
        return _response(500, {"error": str(e)})
