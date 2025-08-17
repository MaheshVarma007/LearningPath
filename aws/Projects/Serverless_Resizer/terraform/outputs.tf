output "bucket_name" {
  value       = aws_s3_bucket.images.bucket
  description = "S3 bucket for originals and thumbnails"
}

output "api_invoke_url" {
  value       = aws_apigatewayv2_api.http.api_endpoint
  description = "Base URL for HTTP API (POST /presign)"
}

output "uploader_lambda_arn" {
  value       = aws_lambda_function.uploader.arn
  description = "ARN of the uploader Lambda function"
}

output "resizer_lambda_arn" {
  value       = aws_lambda_function.resizer.arn
  description = "ARN of the resizer Lambda function"
}

output "originals_prefix" {
  value = local.originals_prefix
}

output "thumbnails_prefix" {
  value = local.thumbnails_prefix
}
