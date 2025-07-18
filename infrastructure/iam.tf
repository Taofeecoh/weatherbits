resource "aws_iam_user" "airflow_tao" {
  name = "Airflow-Tao"

}

resource "aws_iam_policy" "airflow_policy_tao2" {
  name        = "airflow-policy-tao2"
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
          "s3:HeadObject"
        ],
        Resource = ["arn:aws:s3:::tao-general-ingestion2/*"]
      }
    ]
  })
}

resource "aws_iam_user_policy_attachment" "airflow" {
  user       = aws_iam_user.airflow_tao.name
  policy_arn = aws_iam_policy.airflow_policy_tao2.arn
}


resource "aws_iam_access_key" "airflow_tao" {
  user = aws_iam_user.airflow_tao.name
}


resource "aws_ssm_parameter" "airflow_tao_KeyID" {
  name  = "airflow_tao_KeyID"
  type  = "String"
  value = aws_iam_access_key.airflow_tao.id
}


resource "aws_ssm_parameter" "airflow_tao_secretKey" {
  name  = "airflow_tao_secretKey"
  type  = "SecureString"
  value = aws_iam_access_key.airflow_tao.secret
}
