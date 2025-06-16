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

resource "aws_ssm_parameter" "airflow_tao_KeyIDtest" {
  name  = "airflow_tao_KeyIDtest"
  type  = "String"
  value = aws_iam_access_key.airflow_tao.id
}