
variable "app" {
  description = "Application name"
  type        = string
}

# variable "app_version" {
#   description = "Application version"
#   type        = string
# }

variable "runtime" {
  description = "Application runtime"
  type        = string
  default     = "python3.8"
}

variable "region" {
  description = "AWS region"
  type        = string
  default     = "ap-southeast-2"
}

variable "auth_key" {
  description = "Authentication"
  type        = string
}

variable "env" {
  description = "Environment"
  type        = string
  default     = "dev"
}
