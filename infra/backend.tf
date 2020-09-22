
terraform {
  backend "s3" {
    bucket         = "hello.terraform.state"
    key            = "terraform.tfstate"
    region         = "ap-southeast-2"
    encrypt        = true
    dynamodb_table = "hello-terraform-locks"
  }
}