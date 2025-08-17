locals {
  name_prefix = "${var.project}-${var.env}"
  # S3 key prefixes
  originals_prefix  = "originals/"
  thumbnails_prefix = "thumbnails/"
}

############################
# S3 bucket (versioned + CORS)
############################

resource "aws_s3_bucket" "images" {
  bucket = var.bucket_name != "" ? var.bucket_name : "${var.project}-${var.env}-${random_id.bucket_id.hex}"
}

resource "random_id" "bucket_id" {
  byte_length = 4
}

resource "aws_s3_bucket_versioning" "images" {
  bucket = aws_s3_bucket.images.id
  versioning_configuration { status = "Enabled" }
}

# Block all public ACLs (we use presigned URLs for uploads)
resource "aws_s3_bucket_public_access_block" "images" {
  bucket                  = aws_s3_bucket.images.id
  block_public_acls       = true
  ignore_public_acls      = true
  block_public_policy     = true
  restrict_public_buckets = true
}

# CORS so browsers can PUT with presigned URL and GET images
resource "aws_s3_bucket_cors_configuration" "images" {
  bucket = aws_s3_bucket.images.id
  cors_rule {
    allowed_methods = ["PUT", "GET", "HEAD"]
    allowed_origins = var.cors_allowed_origins
    allowed_headers = ["*"]
    expose_headers  = ["ETag"]
    max_age_seconds = 300
  }
}

# (Optional but recommended) default SSE
resource "aws_s3_bucket_server_side_encryption_configuration" "images" {
  bucket = aws_s3_bucket.images.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

############################
# IAM assume role policy for Lambda
############################
data "aws_iam_policy_document" "lambda_assume" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}

############################
# Uploader Lambda: presigned PUT URLs
############################
data "aws_iam_policy_document" "uploader_policy" {
  statement {
    sid     = "WriteOriginals"
    actions = ["s3:PutObject"]
    resources = [
      "${aws_s3_bucket.images.arn}/${local.originals_prefix}*"
    ]
  }

  statement {
    sid     = "Logs"
    actions = ["logs:CreateLogGroup", "logs:CreateLogStream", "logs:PutLogEvents"]
    resources = ["*"]
  }
}

resource "aws_iam_role" "uploader_role" {
  name               = "${local.name_prefix}-uploader-role"
  assume_role_policy = data.aws_iam_policy_document.lambda_assume.json
}

resource "aws_iam_role_policy" "uploader_inline" {
  name   = "${local.name_prefix}-uploader-policy"
  role   = aws_iam_role.uploader_role.id
  policy = data.aws_iam_policy_document.uploader_policy.json
}

# NOTE: CI should place the zip at ../build/uploader.zip
resource "aws_lambda_function" "uploader" {
  function_name = "${local.name_prefix}-uploader"
  role          = aws_iam_role.uploader_role.arn
  handler       = "app.handler"
  runtime       = "python3.12"
  filename      = "../build/uploader.zip"

  # ensure code updates trigger a new deployment
  #source_code_hash = filebase64sha256("${path.module}/../build/uploader.zip")

  environment {
    variables = {
      BUCKET = aws_s3_bucket.images.bucket
    }
  }
  timeout = 15
}

############################
# API Gateway (HTTP API) -> Uploader Lambda
############################
resource "aws_apigatewayv2_api" "http" {
  name          = "${local.name_prefix}-api"
  protocol_type = "HTTP"
}

resource "aws_apigatewayv2_integration" "uploader_integration" {
  api_id                 = aws_apigatewayv2_api.http.id
  integration_type       = "AWS_PROXY"
  integration_uri        = aws_lambda_function.uploader.arn
  payload_format_version = "2.0"
}

resource "aws_apigatewayv2_route" "post_presign" {
  api_id    = aws_apigatewayv2_api.http.id
  route_key = "POST /presign"
  target    = "integrations/${aws_apigatewayv2_integration.uploader_integration.id}"
}

resource "aws_lambda_permission" "allow_apigw_invoke_uploader" {
  statement_id  = "AllowAPIGWInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.uploader.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.http.execution_arn}/*/*"
}

resource "aws_apigatewayv2_stage" "default" {
  api_id      = aws_apigatewayv2_api.http.id
  name        = "$default"
  auto_deploy = true
}

############################
# Resizer Lambda: S3 event trigger
############################
data "aws_iam_policy_document" "resizer_policy" {
  statement {
    sid     = "ReadOriginals"
    actions = ["s3:GetObject"]
    resources = [
      "${aws_s3_bucket.images.arn}/${local.originals_prefix}*"
    ]
  }
  statement {
    sid     = "WriteThumbnails"
    actions = ["s3:PutObject"]
    resources = [
      "${aws_s3_bucket.images.arn}/${local.thumbnails_prefix}*"
    ]
  }
  statement {
    sid     = "Logs"
    actions = ["logs:CreateLogGroup", "logs:CreateLogStream", "logs:PutLogEvents"]
    resources = ["*"]
  }
}

resource "aws_iam_role" "resizer_role" {
  name               = "${local.name_prefix}-resizer-role"
  assume_role_policy = data.aws_iam_policy_document.lambda_assume.json
}

resource "aws_iam_role_policy" "resizer_inline" {
  name   = "${local.name_prefix}-resizer-policy"
  role   = aws_iam_role.resizer_role.id
  policy = data.aws_iam_policy_document.resizer_policy.json
}

# NOTE: CI should place the zip at ../build/resizer.zip
resource "aws_lambda_function" "resizer" {
  function_name = "${local.name_prefix}-resizer"
  role          = aws_iam_role.resizer_role.arn
  handler       = "app.handler"
  runtime       = "python3.12"
  filename      = "../build/resizer.zip"

  #source_code_hash = filebase64sha256("${path.module}/../build/resizer.zip")

  environment {
    variables = {
      BUCKET       = aws_s3_bucket.images.bucket
      THUMB_WIDTH  = tostring(var.thumb_width)
      SRC_PREFIX   = local.originals_prefix
      DEST_PREFIX  = local.thumbnails_prefix
    }
  }
  timeout = 30
}

# Allow S3 to invoke the resizer Lambda
resource "aws_lambda_permission" "allow_s3_invoke_resizer" {
  statement_id  = "AllowS3Invoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.resizer.function_name
  principal     = "s3.amazonaws.com"
  source_arn    = aws_s3_bucket.images.arn
}

# S3 -> Lambda notification for object created under originals/
resource "aws_s3_bucket_notification" "images_events" {
  bucket = aws_s3_bucket.images.id

  lambda_function {
    lambda_function_arn = aws_lambda_function.resizer.arn
    events              = ["s3:ObjectCreated:*"]
    filter_prefix       = local.originals_prefix
  }

  depends_on = [aws_lambda_permission.allow_s3_invoke_resizer]
}
