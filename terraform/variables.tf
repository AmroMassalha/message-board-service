variable "docker_username" {
  description = "DockerHub Username"
  type        = string
  sensitive   = true
}

variable "docker_password" {
  description = "DockerHub Password"
  type        = string
  sensitive   = true
}
