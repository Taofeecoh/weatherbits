resource "aws_s3_bucket" "general" {
  bucket        = "tao-general-ingestion"
  force_destroy = true

  tags = {
    Name        = "tao-general-ingestion"
    Environment = "Dev"
    Accessed_by = "Airflow"
  }
}

resource "aws_s3_bucket_versioning" "versioning_general" {
  bucket = aws_s3_bucket.general.id
  versioning_configuration {
    status = "Enabled"
  }
}