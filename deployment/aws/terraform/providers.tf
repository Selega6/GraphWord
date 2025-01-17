provider "docker" {
  host = "npipe:////./pipe/docker_engine"
}


provider "aws" {
  access_key                  = "test"
  secret_key                  = "test"
  region                      = "us-east-1"
  skip_credentials_validation = true
  skip_metadata_api_check     = true
  skip_requesting_account_id  = true
  endpoints {
    s3     = "http://localhost:4566"
    lambda = "http://localhost:4566"
    iam    = "http://localhost:4566"
    events = "http://localhost:4566"
    sqs    = "http://localhost:4566"
    eventbridge = "http://localhost:4566"
  }
}
