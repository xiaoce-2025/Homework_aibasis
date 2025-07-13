#!/bin/bash

# 严小希AI助手 - 后端部署脚本
echo "开始部署后端服务..."

# 创建项目目录
sudo mkdir -p /var/www/yanxx-ai
sudo chown $USER:$USER /var/www/yanxx-ai

# 进入项目目录
cd /var/www/yanxx-ai

# 克隆项目（如果还没有）
if [ ! -d "backend" ]; then
    git clone https://github.com/xiaoce-2025/aibasis_homework.git .
fi

# 创建Python虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装Python依赖
cd backend
pip install -r requirements.txt

# 创建生产环境配置文件
cat > config_prod.py << EOF
# 生产环境配置
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here'
    DEBUG = False
    HOST = '0.0.0.0'
    PORT = 5000
    
    # 数据库配置
    DATABASE_URL = '/var/www/yanxx-ai/backend/db.json'
    
    # AI服务配置
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    SILICON_FLOW_API_KEY = os.environ.get('SILICON_FLOW_API_KEY')
    
    # 跨域配置
    CORS_ORIGINS = ['http://your-domain.com', 'https://your-domain.com']
EOF

# 创建Gunicorn配置文件
cat > gunicorn.conf.py << EOF
# Gunicorn配置
bind = "0.0.0.0:5000"
workers = 4
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2
max_requests = 1000
max_requests_jitter = 100
preload_app = True
EOF

# 安装Gunicorn
pip install gunicorn

# 创建systemd服务文件
sudo tee /etc/systemd/system/yanxx-backend.service > /dev/null << EOF
[Unit]
Description=Yanxx AI Backend
After=network.target

[Service]
Type=notify
User=www-data
Group=www-data
WorkingDirectory=/var/www/yanxx-ai/backend
Environment=PATH=/var/www/yanxx-ai/venv/bin
ExecStart=/var/www/yanxx-ai/venv/bin/gunicorn -c gunicorn.conf.py Api:app
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# 设置权限
sudo chown -R www-data:www-data /var/www/yanxx-ai
sudo chmod -R 755 /var/www/yanxx-ai

# 启动服务
sudo systemctl daemon-reload
sudo systemctl enable yanxx-backend
sudo systemctl start yanxx-backend

echo "后端服务部署完成！"
echo "服务状态：sudo systemctl status yanxx-backend" 