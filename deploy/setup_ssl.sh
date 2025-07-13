#!/bin/bash

# 严小希AI助手 - SSL证书配置脚本
echo "开始配置SSL证书..."

# 安装Certbot
sudo apt install certbot python3-certbot-nginx -y

# 获取SSL证书
sudo certbot --nginx -d your-domain.com -d www.your-domain.com

# 设置自动续期
sudo crontab -l 2>/dev/null | { cat; echo "0 12 * * * /usr/bin/certbot renew --quiet"; } | sudo crontab -

echo "SSL证书配置完成！"
echo "访问地址：https://your-domain.com" 