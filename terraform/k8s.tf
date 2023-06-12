locals {
  dockerhub_secret_yaml = templatefile("${path.module}/assets/docker-registry/dockerhub-secret.yaml.tpl", {
    namespace = kubernetes_namespace.docker-registry.metadata[0].name
    username  = base64encode(var.docker_username)
    password  = base64encode(var.docker_password)
  })
}

resource "kubernetes_namespace" "docker-registry" {
  metadata {
    name = "docker-registry"
  }
}

resource "kubernetes_manifest" "dockerhub_secret" {
  manifest = yamldecode(local.dockerhub_secret_yaml)
}
