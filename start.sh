#!/bin/bash

echo "========================================="
echo "  视频文字提取工具 - Replit 版本"
echo "========================================="
echo ""

# 创建必要的文件夹
mkdir -p uploads downloads

# 安装 Python 依赖
echo "[1/4] 安装 Python 依赖..."
pip install -r requirements.txt --quiet

# 安装 Node.js 依赖
echo "[2/4] 安装 Node.js 依赖..."
npm install --silent

# 构建前端
echo "[3/4] 构建前端..."
npm run build

# 启动后端
echo "[4/4] 启动服务..."
echo ""
echo "========================================="
echo "  ✅ 服务启动成功！"
echo "========================================="
echo ""
echo "访问地址会在 Replit 顶部显示"
echo ""

# 同时启动前端和后端
python app.py &
npx serve dist -l 3000
