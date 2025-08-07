# === Build stage ===
FROM node:18-alpine AS build

WORKDIR /app

# 安裝依賴（利用快取）
COPY package*.json ./
RUN npm install

# 加入本地 node_modules/.bin 到 PATH，讓 npm run build 可以執行 tsc
ENV PATH /app/node_modules/.bin:$PATH

# 複製全部專案檔案
COPY . .

# 建置（包含 tsc -b 和 vite build）
RUN npm run build

# === Production stage ===
FROM nginx:alpine

# 複製打包好的前端檔案到 Nginx 目錄
COPY --from=build /app/dist /usr/share/nginx/html

# 開啟埠
EXPOSE 80

# 啟動 nginx
CMD ["nginx", "-g", "daemon off;"]
