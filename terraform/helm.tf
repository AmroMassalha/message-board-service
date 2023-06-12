resource "helm_release" "docker_pull_cache" {
  depends_on = [ kubernetes_manifest.dockerhub_secret ]
  name             = "docker-pull-cache"
  repository       = "https://helm.twun.io"
  chart            = "docker-registry"
  namespace        = kubernetes_namespace.docker-registry.metadata[0].name
  values = [
    "${file("./assets/docker-registry/values.yaml")}"
  ]
}

resource "helm_release" "argo_workflows" {
  name = "argo-workflows"
  namespace = "argo"
  create_namespace = true
  repository = "https://argoproj.github.io/argo-helm"
  chart = "argo-workflows"
}
