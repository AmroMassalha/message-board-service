apiVersion: v1
kind: Secret
metadata:
  name: dockerhub-secret
  namespace: ${namespace}
type: Opaque
data:
  proxyUsername: ${username}
  proxyPassword: ${password}
