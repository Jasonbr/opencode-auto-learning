#!/bin/bash
# Final push script

set -e

cd ~/opencode-auto-learning

echo "🚀 推送到 GitHub..."
echo ""

# 确保 remote 正确
git remote remove origin 2>/dev/null || true
git remote add origin https://github.com/Jasonbr/opencode-auto-learning.git

echo "Remote:"
git remote -v
echo ""

# 推送
echo "正在推送..."
git push -u origin main

echo ""
echo "✅ 推送成功！"
echo ""
echo "访问你的仓库:"
echo "  https://github.com/Jasonbr/opencode-auto-learning"
echo ""

# 创建标签
echo "创建 Release 标签 v1.0.0..."
git tag v1.0.0
git push origin v1.0.0

echo ""
echo "🎉 全部完成！"
echo ""
echo "访问: https://github.com/Jasonbr/opencode-auto-learning/releases"
