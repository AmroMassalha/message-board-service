resource "helm_release" "docker_pull_cache" {
  name             = "docker-pull-cache"
  repository       = "https://helm.twun.io"
  chart            = "docker-registry"
  namespace        = "docker-registry"
  create_namespace = true
  values = [
    "${file("./assets/docker-registry/values.yaml")}"
  ]
}
