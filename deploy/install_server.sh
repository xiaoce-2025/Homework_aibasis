#!/bin/bash

# 严小希AI助手 - 服务器部署脚本
echo "开始安装服务器环境..."

# 更新系统
sudo apt update && sudo apt upgrade -y

# 安装Python 3.8+
sudo apt install python3 python3-pip python3-venv -y

# 安装Node.js 16+
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# 安装Nginx
sudo apt install nginx -y

# 安装Git
sudo apt install git -y

# 安装系统依赖（用于PaddleOCR等）
sudo apt install libgl1-mesa-glx libglib2.0-0 libsm6 libxext6 libxrender-dev libgomp1 -y

# 安装Redis（可选，用于缓存）
sudo apt install redis-server -y

echo "服务器环境安装完成！" 