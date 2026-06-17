#!/bin/bash
# WatchAlert 邮件问题本地排查脚本
# 请在服务器上运行此脚本

echo "=========================================="
echo "🔍 WatchAlert 邮件问题排查脚本"
echo "=========================================="
echo ""

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${YELLOW}请在服务器上运行此脚本${NC}"
echo ""

# 1. 检查 Docker
echo "1️⃣  检查 Docker 状态..."
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker 未安装${NC}"
    exit 1
fi

# 检查 w8t-service 容器
if docker ps | grep -q "w8t-service"; then
    echo -e "${GREEN}✅ w8t-service 运行中${NC}"
    docker ps | grep w8t-service
else
    echo -e "${RED}❌ w8t-service 未运行${NC}"
    echo "尝试查找 w8t 相关容器..."
    docker ps -a | grep -i "w8t" || echo "未找到 w8t 容器"
fi

echo ""

# 2. SMTP 连接测试
echo "2️⃣  SMTP 连接测试..."
if timeout 5 bash -c '</dev/tcp/smtp.qiye.aliyun.com/465' 2>/dev/null; then
    echo -e "${GREEN}✅ smtp.qiye.aliyun.com:465 可连接${NC}"
else
    echo -e "${RED}❌ smtp.qiye.aliyun.com:465 连接失败${NC}"
    echo "   尝试 ping..."
    ping -c 1 smtp.qiye.aliyun.com | head -2
fi

echo ""

# 3. 检查邮件日志
echo "3️⃣  检查邮件相关日志..."
CONTAINER=$(docker ps --format "{{.Names}}" | grep -i w8t | head -1)

if [ -n "$CONTAINER" ]; then
    echo "检查容器: $CONTAINER"
    
    # 获取最近 50 行包含 email/smtp 的日志
    LOGS=$(docker logs "$CONTAINER" 2>&1 | grep -i "email\|smtp\|mail\|邮件\|发送" | tail -20)
    
    if [ -n "$LOGS" ]; then
        echo "最近邮件相关日志:"
        echo "$LOGS"
    else
        echo -e "${YELLOW}⚠️  未找到邮件相关日志${NC}"
    fi
    
    echo ""
    echo "获取错误日志:"
    ERRORS=$(docker logs "$CONTAINER" 2>&1 | grep -i "error\|fail\|err\|失败" | tail -10)
    if [ -n "$ERRORS" ]; then
        echo "$ERRORS"
    else
        echo "无错误日志"
    fi
else
    echo -e "${RED}❌ 未找到 w8t 容器${NC}"
fi

echo ""

# 4. MySQL 配置检查
echo "4️⃣  MySQL 配置检查..."

# 检查 MySQL 是否运行
if command -v mysql &> /dev/null; then
    echo "MySQL 客户端可用"
    
    # 尝试连接 (用户需要输入密码)
    echo "检查 settings 表中的邮件配置..."
    mysql -u root -p watchalert -e "
        SELECT 'settings' as table_name, 
               JSON_EXTRACT(email_config, '\$.serverAddress') as smtp_server,
               JSON_EXTRACT(email_config, '\$.port') as port,
               JSON_EXTRACT(email_config, '\$.email') as email
        FROM settings 
        WHERE id=1;
    " 2>/dev/null || echo "需要密码，请手动检查"
    
    echo ""
    echo "检查邮件模板..."
    mysql -u root -p watchalert -e "
        SELECT id, template_type, LENGTH(template) as template_length
        FROM notice_template_examples
        WHERE template_type = 'Email'
        LIMIT 3;
    " 2>/dev/null || echo "需要密码"
else
    echo -e "${YELLOW}⚠️  MySQL 客户端未安装${NC}"
fi

echo ""

# 5. 配置文件检查
echo "5️⃣  配置文件检查..."
WATCHALERT_CONFIG="/opt/watchalert/config.yaml"
if [ -f "$WATCHALERT_CONFIG" ]; then
    echo "找到配置文件: $WATCHALERT_CONFIG"
    echo "邮件配置部分:"
    grep -i "email\|smtp\|mail" "$WATCHALERT_CONFIG" | head -10 || echo "配置中未找到邮件相关配置"
else
    echo "未找到配置文件: $WATCHALERT_CONFIG"
fi

echo ""

# 6. 网络诊断
echo "6️⃣  网络诊断..."
echo "测试到阿里云 SMTP 的网络..."
ping -c 2 smtp.qiye.aliyun.com | grep -E "PING|packets|rtt" || echo "ping 失败"

echo ""
echo "检查 DNS..."
nslookup smtp.qiye.aliyun.com | head -5 || dig smtp.qiye.aliyun.com +short || echo "DNS 查询失败"

echo ""
echo "=========================================="
echo "📊 诊断结果"
echo "=========================================="
echo ""
echo "请查看上述输出，特别关注："
echo "  1. ❌ 标记的错误"
echo "  2. 邮件相关的日志输出"
echo "  3. SMTP 连接状态"
echo ""
echo "常见问题："
echo "  - 认证失败：检查邮箱密码是否正确"
echo "  - 连接失败：检查网络/防火墙设置"
echo "  - 模板为空：重新设置邮件模板"
echo ""
echo "下一步建议："
echo "  1. 登录阿里云邮箱管理后台检查密码"
echo "  2. 更新 MySQL 中的 email_config"
echo "  3. 重启 w8t-service"
echo ""