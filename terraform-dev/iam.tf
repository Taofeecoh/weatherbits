resource "aws_iam_user" "airflow_tao" {
  name = "Airflow-Tao"

  tags = {
    Group = "Airflow"
  }
}

resource "aws_iam_policy" "airflow_policy_tao" {
  name        = "airflow-policy-tao"
  description = "Policy desciption for user: Airflow-Tao"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid      = "ListBucketAccess"
        Effect   = "Allow",
        Action   = ["s3:ListAllMyBuckets"],
        Resource = "*"
      },
      {
        Sid    = "PutObjectsAccess"
        Effect = "Allow",
        Action = [
          "s3:ListBucket",
          "s3:PutObject",
          "s3:GetObject",
          "s3:HeadObject"
        ],
        Resource = ["arn:aws:s3:::tao-weatherbits-ingestion/*"]
      }
    ]
  })
}

resource "aws_iam_user_policy_attachment" "airflow" {
  user       = aws_iam_user.airflow_tao.name
  policy_arn = aws_iam_policy.airflow_policy_tao.arn
}


resource "aws_iam_access_key" "airflow_tao" {
  user = aws_iam_user.airflow_tao.name
}
