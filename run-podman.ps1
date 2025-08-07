# 使用 Podman 運行 React 應用程式

# 使用 docker-compose (podman-compose)
podman-compose up --build

# 或者單獨使用 Podman 命令：
# 1. 構建映像
# podman build -t antd-self-introduction .

# 2. 運行容器
# podman run -d --name antd-self-introduction -p 3000:80 antd-self-introduction

# 停止和清理
# podman-compose down
# podman rmi antd-self-introduction
