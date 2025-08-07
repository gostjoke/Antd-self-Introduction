# Podman 部署指南

## 前置需求

1. 安裝 Podman
2. 安裝 podman-compose：
   ```powershell
   pip install podman-compose
   ```

## 快速啟動

### 方法 1: 使用腳本（推薦）
```powershell
.\run-podman.ps1
```

### 方法 2: 使用 podman-compose
```powershell
# 構建並啟動
podman-compose up --build -d

# 查看狀態
podman-compose ps

# 停止服務
podman-compose down
```

### 方法 3: 純 Podman 命令
```powershell
# 構建映像
podman build -t antd-self-introduction .

# 運行容器 (綁定到所有網路介面)
podman run -d --name antd-self-introduction -p 0.0.0.0:3000:80 antd-self-introduction

# 檢查容器狀態
podman ps

# 停止並刪除容器
podman stop antd-self-introduction
podman rm antd-self-introduction
```

## 訪問應用程式

- **本地訪問**: http://localhost:3000
- **網路訪問**: http://[您的IP地址]:3000

## 故障排除

### 查看容器日誌
```powershell
# 使用 compose
podman-compose logs

# 使用 podman
podman logs antd-self-introduction
```

### 進入容器調試
```powershell
podman exec -it antd-self-introduction /bin/sh
```

### 檢查埠占用
```powershell
netstat -an | findstr :3000
```

## 重要設定說明

- **埠綁定**: `0.0.0.0:3000:80` 確保從任何 IP 都能訪問
- **Nginx 配置**: 支援 SPA 路由和靜態資源緩存
- **多階段構建**: 減少最終映像大小
- **日誌掛載**: nginx 日誌保存到本地 `./logs` 目錄
