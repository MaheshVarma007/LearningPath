import os, io, boto3, logging
from PIL import Image, ImageOps

log = logging.getLogger()
log.setLevel(logging.INFO)

s3 = boto3.client("s3")
BUCKET       = os.environ.get("BUCKET", "img-resizer-dev-ee03ffe6")
THUMB_WIDTH  = int(os.environ.get("THUMB_WIDTH", "256"))
SRC_PREFIX   = os.environ.get("SRC_PREFIX", "originals/")
DEST_PREFIX  = os.environ.get("DEST_PREFIX", "thumbnails/")

def _resize(img, width):
    img = ImageOps.exif_transpose(img)  # correct orientation if present
    w, h = img.size
    if w <= width:
        return img
    new_h = max(1, int(h * (width / float(w))))
    return img.resize((width, new_h), Image.LANCZOS)

def handler(event, context):
    for rec in event.get("Records", []):
        bucket = rec["s3"]["bucket"]["name"]
        key    = rec["s3"]["object"]["key"]

        if not key.startswith(SRC_PREFIX):
            log.info("Ignoring key (prefix mismatch): %s", key)
            continue

        try:
            # download to memory
            obj = s3.get_object(Bucket=bucket, Key=key)
            img = Image.open(io.BytesIO(obj["Body"].read()))

            # resize
            img = _resize(img, THUMB_WIDTH)

            # save to memory
            out = io.BytesIO()
            img.save(out, format="JPEG", quality=85, optimize=True)
            out.seek(0)

            # put thumbnail
            out_key = key.replace(SRC_PREFIX, DEST_PREFIX, 1)
            s3.put_object(
                Bucket=BUCKET,
                Key=out_key,
                Body=out,
                ContentType="image/jpeg",
                Metadata={"source": key},
            )
            log.info("Wrote thumbnail: s3://%s/%s", BUCKET, out_key)
        except Exception as e:
            log.exception("Failed processing %s: %s", key, e)
    return {"statusCode": 200}