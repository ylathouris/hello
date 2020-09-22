
resource "aws_ssm_parameter" "secret" {
  name        = "/hello/auth-key"
  description = "Secret key used for authenticating hello users"
  type        = "SecureString"
  value       = base64encode(var.auth_key)

  tags = {
    "app:name"     = var.app,
  }
}
