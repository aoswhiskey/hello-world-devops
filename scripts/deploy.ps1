param(
    [string]$Image = "aoswhiskey/hello-world-devops:1.0.0"
)

$ErrorActionPreference = "Stop"

docker build -t $Image .
minikube image load $Image
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl rollout status deployment/hello-world --timeout=120s
kubectl get pods -l app=hello-world -o wide
kubectl get service hello-world

Write-Host "Run the following command in a separate terminal:"
Write-Host "kubectl port-forward service/hello-world 32777:32777"
Write-Host "Then open http://127.0.0.1:32777"
