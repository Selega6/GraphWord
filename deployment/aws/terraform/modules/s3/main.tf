resource "aws_s3_bucket" "graphword_bucket" {
  bucket = var.bucket_name
}

#subir api_code.zip al bucket
resource "aws_s3_object" "api_code" {
  bucket = aws_s3_bucket.graphword_bucket.bucket
  key    = "api_code.zip"
  source = "api_code.zip"
  content_type = "application/zip"  
}
