# 严小希AI助手 - 服务器部署指南

## 📋 部署前准备

### 1. 服务器要求
- **操作系统**：Ubuntu 20.04+ 或 CentOS 7+
- **内存**：至少2GB RAM（推荐4GB+）
- **存储**：至少10GB可用空间
- **网络**：公网IP地址
- **域名**：已解析到服务器IP

### 2. 必需的服务
- **AI服务API密钥**：
  - OpenAI API密钥（用于AI对话、续写等功能）
  - 硅基流动API密钥（用于文本转语音）

## 🚀 快速部署

### 方法一：一键部署（推荐）

1. **上传部署文件到服务器**
```bash
# 在本地打包部署文件
tar -czf deploy.tar.gz deploy/

# 上传到服务器
scp deploy.tar.gz user@your-server-ip:~/
```

2. **在服务器上执行部署**
```bash
# 解压文件
tar -xzf deploy.tar.gz
cd deploy

# 执行一键部署
chmod +x deploy_all.sh
./deploy_all.sh
```

3. **按提示输入信息**
- 域名地址
- API密钥（可选）

### 方法二：Docker部署

1. **安装Docker和Docker Compose**
```bash
# 安装Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# 安装Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

2. **配置环境变量**
```bash
# 创建.env文件
cat > .env << EOF
OPENAI_API_KEY=your-openai-api-key
SILICON_FLOW_API_KEY=your-silicon-flow-api-key
SECRET_KEY=$(openssl rand -hex 32)
EOF
```

3. **启动服务**
```bash
docker-compose up -d
```

## 🔧 手动部署步骤

### 1. 安装服务器环境
```bash
chmod +x install_server.sh
./install_server.sh
```

### 2. 部署后端服务
```bash
chmod +x deploy_backend.sh
./deploy_backend.sh
```

### 3. 部署前端应用
```bash
chmod +x deploy_frontend.sh
./deploy_frontend.sh
```

### 4. 配置SSL证书
```bash
chmod +x setup_ssl.sh
./setup_ssl.sh
```

## 📊 服务管理

### 查看服务状态
```bash
# 后端服务
sudo systemctl status yanxx-backend

# Nginx服务
sudo systemctl status nginx

# 查看日志
sudo journalctl -u yanxx-backend -f
```

### 重启服务
```bash
# 重启后端
sudo systemctl restart yanxx-backend

# 重启Nginx
sudo systemctl restart nginx

# 重新加载Nginx配置
sudo nginx -s reload
```

### 更新代码
```bash
# 进入项目目录
cd /var/www/yanxx-ai

# 拉取最新代码
git pull

# 重启服务
sudo systemctl restart yanxx-backend
```

## 🔒 安全配置

### 1. 防火墙设置
```bash
# 允许HTTP和HTTPS
sudo ufw allow 80
sudo ufw allow 443

# 启用防火墙
sudo ufw enable
```

### 2. 定期备份
```bash
# 创建备份脚本
cat > /var/www/yanxx-ai/backup.sh << 'EOF'
#!/bin/bash
BACKUP_DIR="/var/backups/yanxx-ai"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

# 备份数据库
cp /var/www/yanxx-ai/backend/db.json $BACKUP_DIR/db_$DATE.json

# 备份配置文件
tar -czf $BACKUP_DIR/config_$DATE.tar.gz /etc/nginx/sites-available/yanxx-ai

echo "备份完成：$BACKUP_DIR"
EOF

chmod +x /var/www/yanxx-ai/backup.sh

# 添加到定时任务
echo "0 2 * * * /var/www/yanxx-ai/backup.sh" | sudo crontab -
```

## 🐛 故障排除

### 常见问题

1. **后端服务无法启动**
```bash
# 检查日志
sudo journalctl -u yanxx-backend -f

# 检查端口占用
sudo netstat -tlnp | grep :5000

# 检查权限
sudo chown -R www-data:www-data /var/www/yanxx-ai
```

2. **前端无法访问**
```bash
# 检查Nginx状态
sudo systemctl status nginx

# 检查Nginx配置
sudo nginx -t

# 检查防火墙
sudo ufw status
```

3. **API请求失败**
```bash
# 检查后端服务
curl http://localhost:5000/api/ConnectTest

# 检查日志
sudo journalctl -u yanxx-backend -f
```

### 性能优化

1. **启用Gzip压缩**
```bash
# 在Nginx配置中添加
gzip on;
gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;
```

2. **配置缓存**
```bash
# 静态资源缓存
location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
}
```

3. **数据库优化**
```bash
# 定期清理日志
sudo journalctl --vacuum-time=7d
```

## 📞 技术支持

如果遇到问题，请：

1. 查看服务日志
2. 检查配置文件
3. 确认网络连接
4. 联系技术支持

---

**部署完成后，您就可以通过 https://your-domain.com 访问严小希AI助手了！** 🎉 