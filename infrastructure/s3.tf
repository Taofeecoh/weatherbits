resource "aws_s3_bucket" "general" {
  bucket        = "tao-general-ingestion2"
  force_destroy = true

  tags = {
    Name        = "tao-general-ingestion2"
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