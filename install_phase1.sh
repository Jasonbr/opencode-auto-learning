#!/bin/bash
# Phase 1 安装脚本

set -e

echo "🚀 Installing Phase 1: Rule-Learning Integration"

# 检查目录
if [ ! -d "~/opencode-auto-learning" ]; then
    echo "❌ opencode-auto-learning not found"
    exit 1
fi

# 创建规则集成目录
mkdir -p ~/opencode-auto-learning/src/rules_integration

# 安装依赖
echo "📦 Installing dependencies..."
pip3 install -q requests mem0ai networkx 2>/dev/null || echo "Some packages already installed"

# 创建配置文件
cat > ~/opencode-auto-learning/config/rules_config.json << 'CONFIG'
{
    "enabled": true,
    "track_tdd": true,
    "track_precommit": true,
    "track_three_strikes": true,
    "auto_save": true,
    "mem0_config": {
        "api_key": "${MEM0_API_KEY}",
        "user_id": "opencode-user"
    }
}
CONFIG

echo "✅ Configuration created"

# 测试导入
echo "🧪 Testing imports..."
python3 -c "
import sys
sys.path.insert(0, '~/opencode-auto-learning/src')
from rules_integration import RuleTracker
print('✅ RuleTracker imported successfully')
"

echo ""
echo "🎉 Phase 1 installation complete!"
echo ""
echo "Next steps:"
echo "1. Set MEM0_API_KEY in your environment"
echo "2. Import RuleTracker in your OpenCode session"
echo "3. Start tracking rule executions"
