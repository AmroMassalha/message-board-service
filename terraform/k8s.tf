resource "kubernetes_secret" "dockerhub" {
  metadata {
    name = "dockerhub-creds"
  }

  data = {
    username = var.docker_username
    password = var.docker_password
  }

  type = "kubernetes.io/basic-auth"
}
