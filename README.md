# Hello World DevOps

Тестовое задание: HTTP-приложение на порту `32777`, контейнер Docker и развёртывание в Minikube с двумя репликами.

## Что входит в проект

- `app.py` — HTTP API без сторонних зависимостей;
- `Dockerfile` — образ с непривилегированным пользователем и healthcheck;
- `k8s/deployment.yaml` — Deployment с двумя репликами и probes;
- `k8s/service.yaml` — ClusterIP Service на порту `32777`;
- `diagram.drawio` — редактируемая схема контейнеров и сервиса;
- `screenshots` — подтверждения запуска после выполнения команд.

## Локальная проверка

```powershell
python -m unittest -v
python app.py
```

Открыть <http://127.0.0.1:32777>. Проверка состояния: <http://127.0.0.1:32777/healthz>.

## Docker

```powershell
docker build -t hello-world-devops:1.0.0 .
docker run --rm -p 32777:32777 hello-world-devops:1.0.0
```

Для публикации заменить `DOCKERHUB_USERNAME` на имя пользователя Docker Hub:

```powershell
docker login
docker tag hello-world-devops:1.0.0 DOCKERHUB_USERNAME/hello-world-devops:1.0.0
docker tag hello-world-devops:1.0.0 DOCKERHUB_USERNAME/hello-world-devops:latest
docker push DOCKERHUB_USERNAME/hello-world-devops:1.0.0
docker push DOCKERHUB_USERNAME/hello-world-devops:latest
```

После публикации можно заменить поле `image` в `k8s/deployment.yaml` на `DOCKERHUB_USERNAME/hello-world-devops:1.0.0`.

## Minikube

Для Windows с Docker Desktop:

```powershell
minikube start --driver=docker
docker build -t hello-world-devops:1.0.0 .
minikube image load hello-world-devops:1.0.0
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl rollout status deployment/hello-world --timeout=120s
kubectl get pods -l app=hello-world -o wide
kubectl get service hello-world
```

Проброс порта (команда должна оставаться запущенной):

```powershell
kubectl port-forward service/hello-world 32777:32777
```

После этого открыть <http://127.0.0.1:32777>. Команда `kubectl port-forward service/...` выбирает один из Pod для туннеля; наличие двух готовых реплик проверяется через `kubectl get deployment,pods`.

## Подтверждение результата

![Ответ приложения](screenshots/browser-result.png)

![Состояние Kubernetes](screenshots/kubernetes-status.png)

## Удаление ресурсов

```powershell
kubectl delete -f k8s/service.yaml
kubectl delete -f k8s/deployment.yaml
minikube stop
```
