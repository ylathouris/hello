
provider "aws" {
  version = "~> 2"
  region  = var.region
}

resource "aws_iam_role" "default_role" {
  name               = "${var.app}-role"
  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

resource "aws_iam_role_policy" "default_policy" {
  name   = "default-policy"
  role   = aws_iam_role.default_role.id
  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "arn:*:logs:*:*:*",
      "Effect": "Allow"
    },
    {
      "Action": [
        "ssm:GetParameter"
      ],
      "Resource": "arn:aws:ssm:*:*:parameter/hello/auth-key",
      "Effect": "Allow"
    }
  ]
}
EOF
}

resource "aws_api_gateway_rest_api" "rest_api" {
  name               = var.app
  binary_media_types = ["*"]

  endpoint_configuration {
    types = ["EDGE"]
  }
}

resource "aws_api_gateway_deployment" "rest_api" {
  stage_name  = "api"
  rest_api_id = aws_api_gateway_rest_api.rest_api.id

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_lambda_function" "api_handler" {
  function_name    = "hello"
  runtime          = var.runtime
  handler          = "app.app"
  memory_size      = 128
  timeout          = 10
  source_code_hash = filebase64sha256("${path.module}/deployment.zip")
  filename         = "${path.module}/deployment.zip"
  role             = aws_iam_role.default_role.arn
}

resource "aws_lambda_function" "auth" {
  function_name    = "hello-auth"
  runtime          = var.runtime
  handler          = "app.auth"
  memory_size      = 128
  timeout          = 60
  source_code_hash = filebase64sha256("${path.module}/deployment.zip")
  filename         = "${path.module}/deployment.zip"
  role             = aws_iam_role.default_role.arn
}

resource "aws_lambda_permission" "rest_api_invoke" {
  function_name = "hello"
  action        = "lambda:InvokeFunction"
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.rest_api.execution_arn}/*"
}

resource "aws_lambda_permission" "auth_invoke" {
  function_name = "hello-auth"
  action        = "lambda:InvokeFunction"
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.rest_api.execution_arn}/*"
}

output "url" {
  value = aws_api_gateway_deployment.rest_api.invoke_url
}

output "rest_api_id" {
  value = aws_api_gateway_rest_api.rest_api.id
}
