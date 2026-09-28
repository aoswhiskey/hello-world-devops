$ErrorActionPreference = "Stop"

$deployment = kubectl get deployment hello-world -o json | ConvertFrom-Json
if ($deployment.status.readyReplicas -ne 2) {
    throw "Expected 2 ready replicas, got $($deployment.status.readyReplicas)"
}

$response = Invoke-RestMethod http://127.0.0.1:32777/
if ($response.message -ne "Hello, World!") {
    throw "Unexpected response: $($response | ConvertTo-Json -Compress)"
}

Write-Host "Deployment has 2 ready replicas"
Write-Host ($response | ConvertTo-Json -Compress)
