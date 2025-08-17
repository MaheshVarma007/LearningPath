variable "project" {
  description = "Project slug used for names"
  type        = string
  default     = "img-resizer"
}

variable "env" {
  description = "Environment name"
  type        = string
  default     = "dev"
}

variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "ap-southeast-1"
}

variable "bucket_name" {
  description = "S3 bucket name (must be globally unique). Leave empty to auto-generate."
  type        = string
  default     = ""
}

variable "cors_allowed_origins" {
  description = "Allowed origins for browser uploads (CORS)."
  type        = list(string)
  default     = ["*"] # set to your domain(s) in prod
}

variable "thumb_width" {
  description = "Thumbnail width (px) for the resizer"
  type        = number
  default     = 256
}
