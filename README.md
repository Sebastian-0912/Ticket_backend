
## 架構說明

Mac (Docker Compose) → Minikube (CockroachDB on K8s) 

---

## 安裝 Minikube + MetalLB

### 1.1 啟動 Minikube (使用 Docker Driver)

```bash
minikube start --driver=docker
````

確認狀態：

```bash
minikube status
kubectl config current-context
```

---

### 1.2 安裝 MetalLB

```bash
kubectl apply -f https://raw.githubusercontent.com/metallb/metallb/v0.14.9/config/manifests/metallb-native.yaml
```

---

### 1.3 設定 MetalLB IP Pool

```bash
kubectl apply -f metallb-config.yaml
```

---

## 部署 CockroachDB 到 K8s

### 2.1 CockroachDB StatefulSet + LoadBalancer Service

Apply：

```bash
kubectl apply -f cockroachdb-deployment.yaml
kubectl apply -f cockroachdb-service.yaml
kubectl apply -f cockroachdb-hpa.yaml
```

---

### 2.2 確認 CockroachDB Service

```bash
kubectl get svc cockroachdb
```

---

### 2.3 開啟 Minikube Tunnel

```bash
sudo minikube tunnel
```

**⚠️ 必須保持這個 Terminal 開著，Tunnel 才會持續！**

---

### 2.4 初始化 CockroachDB Cluster

```bash
kubectl exec -it cockroachdb-0 -- ./cockroach init --insecure
```

如果已經初始化過，會看到：

```
ERROR: cluster has already been initialized
```

---

## Docker Compose 部署 Flask + Nginx

### 3.1 `docker-compose.yaml`

---

### 3.2 Flask db url 設定

```env
DATABASE_URL=cockroachdb+psycopg2://root@host.docker.internal:26257/defaultdb?sslmode=disable
```

---

### 3.3 Nginx 設定 `nginx.conf`

---

### 3.4 啟動 Docker Compose

```bash
docker compose up -d
```

---

## 測試

### 4.1 測試 CockroachDB Admin UI

將 CockroachDB Service Port 轉發到本地：

```bash
kubectl port-forward svc/cockroachdb 8088:8080
```

打開訪問：

```
http://localhost:8088
```

---

### 4.2 測試 Flask API

用 curl 測試：

```bash
curl -X POST http://localhost:80/dev/create_all
```
如果失敗則
```bash
docker compose down
docker compose up -d
```
---

