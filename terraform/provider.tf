terraform {
  required_providers {
    helm = {
      source = "hashicorp/helm"
      version = "2.10.1"
    }
    template = {
      source = "hashicorp/template"
      version = "~> 2.2.0"
    }
    kubernetes = {
      source = "hashicorp/kubernetes"
      version = "2.21.1"
    }
  }
}

provider "kubernetes" {
  config_path = "~/.kube/config"
}

provider "helm" {
  kubernetes {
    config_path = "~/.kube/config"
  }
}
