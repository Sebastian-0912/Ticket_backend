# K6 壓力測試使用說明

## 概述
本目錄包含用於測試 Flask 應用自動擴容的 K6 壓力測試腳本。

## 安裝 K6
```bash
# Ubuntu/Debian
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys C5AD17C747E3415A3642D57D77C6C491D6AC1D69
echo "deb https://dl.k6.io/deb stable main" | sudo tee /etc/apt/sources.list.d/k6.list
sudo apt-get update
sudo apt-get install k6

# macOS
brew install k6

# 使用 Docker
docker pull grafana/k6
```

## 測試腳本說明

### test_scale.js
- **目的**: 模擬高流量觸發自動擴容
- **配置**: 50 個虛擬用戶，持續 30 秒
- **目標**: 產生足夠流量觸發 Flask 應用擴容

## 執行測試

### 方法 1: 直接執行
```bash
cd /root/college/dis/Ticket_backend/test
k6 run test_scale.js
```


## 監控結果

### Grafana Dashboard
訪問 **http://localhost:3000/** 查看即時監控數據：

#### 主要監控指標：
1. **Request Rate (requests/min)** - 請求量變化
2. **Active Connections** - 活躍連接數
3. **Flask Instances Count Over Time** - 實例數量變化
4. **Auto-scaling Trigger Thresholds** - 擴容觸發閾值

#### 預期行為：
- 測試開始時：請求量快速上升
- 觸發擴容：Flask 實例數量從 2-3 個增加到 4-5 個
- 測試結束後：實例數量逐漸回到初始狀態

### Dashboard 登入資訊
- URL: http://localhost:3000/
- 用戶名: admin
- 密碼: admin

### 重要面板說明
- **Flask Instances Count Over Time**: 顯示自動擴容效果
- **Request Rate Over Time**: 顯示負載變化
- **Flask Instances Status**: 實時查看各實例狀態
- **Auto-scaling Trigger Thresholds**: 監控擴容觸發條件
