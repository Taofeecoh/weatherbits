resource "aws_ssm_parameter" "airflow_tao_KeyID" {
  name  = "airflow_tao_KeyID"
  type  = "String"
  value = var.airflow_tao_KeyID
}


resource "aws_ssm_parameter" "airflow_tao_secretKey" {
  name  = "airflow_tao_secretKey"
  type  = "SecureString"
  value = var.airflow_tao_secretKey
}