resource "aws_s3_bucket" "weatherbits" {
  bucket        = "tao-weatherbits-ingestion"
  force_destroy = true

  tags = {
    Name        = "tao-weatherbits-ingestion"
    Environment = "Dev"
    Accessed_by = "Airflow"
  }
}

resource "aws_s3_bucket_versioning" "versioning_weatherbits" {
  bucket = aws_s3_bucket.weatherbits.id
  versioning_configuration {
    status = "Enabled"
  }
}