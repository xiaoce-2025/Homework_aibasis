#!/bin/bash

# 严小希AI助手 - 前端部署脚本
echo "开始部署前端应用..."

# 进入项目目录
cd /var/www/yanxx-ai

# 进入前端目录
cd gui

# 安装Node.js依赖
npm install

# 创建生产环境配置文件
cat > .env.production << EOF
# 生产环境配置
NODE_ENV=production
VUE_APP_API_BASE_URL=http://your-domain.com/api
VUE_APP_TITLE=严小希AI助手
EOF

# 构建生产版本
npm run build

# 创建Nginx配置文件
sudo tee /etc/nginx/sites-available/yanxx-ai << EOF
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;
    
    # 前端静态文件
    location / {
        root /var/www/yanxx-ai/gui/dist;
        try_files \$uri \$uri/ /index.html;
        index index.html;
        
        # 缓存静态资源
        location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
            expires 1y;
            add_header Cache-Control "public, immutable";
        }
    }
    
    # API代理到后端
    location /api/ {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        
        # 处理大文件上传
        client_max_body_size 50M;
        proxy_read_timeout 300s;
        proxy_connect_timeout 75s;
    }
    
    # 安全头
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
    add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;
}
EOF

# 启用站点
sudo ln -sf /etc/nginx/sites-available/yanxx-ai /etc/nginx/sites-enabled/

# 测试Nginx配置
sudo nginx -t

# 重启Nginx
sudo systemctl restart nginx

echo "前端应用部署完成！"
echo "访问地址：http://your-domain.com" 