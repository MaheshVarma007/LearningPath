terraform {
  required_version = ">= 1.5.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 5.0"
    }
  }
  cloud { 
    
    organization = "MaheshTFE" 

    workspaces { 
      name = "serverless-resizer" 
    } 
  } 
}


provider "aws" {
  region = var.aws_region
}
