#!/bin/bash

# 严小希AI助手 - 一键部署脚本
echo "=== 严小希AI助手服务器部署 ==="
echo "请确保您已经："
echo "1. 拥有一台Ubuntu服务器"
echo "2. 有域名并已解析到服务器IP"
echo "3. 有AI服务的API密钥"
echo ""

# 检查是否为root用户
if [ "$EUID" -eq 0 ]; then
    echo "请不要使用root用户运行此脚本"
    exit 1
fi

# 设置域名
read -p "请输入您的域名（如：example.com）：" DOMAIN
if [ -z "$DOMAIN" ]; then
    echo "域名不能为空"
    exit 1
fi

# 设置API密钥
read -p "请输入OpenAI API密钥（可选）：" OPENAI_KEY
read -p "请输入硅基流动API密钥（可选）：" SILICON_KEY

# 设置环境变量
export OPENAI_API_KEY=$OPENAI_KEY
export SILICON_FLOW_API_KEY=$SILICON_KEY
export SECRET_KEY=$(openssl rand -hex 32)

echo ""
echo "开始部署..."

# 1. 安装服务器环境
echo "步骤1：安装服务器环境..."
chmod +x deploy/install_server.sh
./deploy/install_server.sh

# 2. 部署后端
echo "步骤2：部署后端服务..."
chmod +x deploy/deploy_backend.sh
./deploy/deploy_backend.sh

# 3. 更新配置文件中的域名
echo "步骤3：更新配置文件..."
sed -i "s/your-domain.com/$DOMAIN/g" /var/www/yanxx-ai/gui/.env.production
sed -i "s/your-domain.com/$DOMAIN/g" /etc/nginx/sites-available/yanxx-ai

# 4. 部署前端
echo "步骤4：部署前端应用..."
chmod +x deploy/deploy_frontend.sh
./deploy/deploy_frontend.sh

# 5. 配置SSL
echo "步骤5：配置SSL证书..."
chmod +x deploy/setup_ssl.sh
./deploy/setup_ssl.sh

echo ""
echo "=== 部署完成！ ==="
echo "访问地址：https://$DOMAIN"
echo "后端API：https://$DOMAIN/api"
echo ""
echo "服务管理命令："
echo "- 查看后端状态：sudo systemctl status yanxx-backend"
echo "- 重启后端：sudo systemctl restart yanxx-backend"
echo "- 查看日志：sudo journalctl -u yanxx-backend -f"
echo "- 重启Nginx：sudo systemctl restart nginx"
echo ""
echo "如需更新代码，请运行："
echo "cd /var/www/yanxx-ai && git pull"
echo "然后重启服务" 