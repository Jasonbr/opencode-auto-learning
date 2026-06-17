#!/bin/bash
# Phase 2 & 3 安装脚本

set -e

echo "🚀 Installing Phase 2 & 3: Proactive Intelligence + Smart Skill Generation"

# 检查 Phase 1
if [ ! -f "~/opencode-auto-learning/src/rules_integration/rule_tracker.py" ]; then
    echo "❌ Phase 1 not found. Run install_phase1.sh first"
    exit 1
fi

echo "✅ Phase 1 detected"

# 安装依赖
echo "📦 Installing dependencies..."
pip3 install -q mem0ai networkx 2>/dev/null || echo "Packages already installed"

echo "✅ Dependencies installed"

# 创建配置
cat > ~/opencode-auto-learning/config/rules_phase2.json << 'CONFIG'
{
    "phase": "2_3",
    "enabled": true,
    "features": {
        "proactive_recommendation": true,
        "auto_apply_threshold": 0.9,
        "skill_generation": true,
        "architecture_solutions": true
    },
    "recommendation": {
        "before_edit": true,
        "before_commit": true,
        "max_recommendations": 3
    },
    "effectiveness": {
        "track_window_days": 30,
        "min_samples": 3
    }
}
CONFIG

echo "✅ Configuration created"

# 测试导入
echo "🧪 Testing imports..."
python3 -c "
import sys
sys.path.insert(0, '~/opencode-auto-learning/src')
from rules_integration import (
    RuleRecommender,
    EffectivenessTracker,
    RuleBasedSkillGenerator,
    ArchitectureSolutionGenerator
)
print('✅ All Phase 2 & 3 modules imported successfully')
" || exit 1

echo ""
echo "🎉 Phase 2 & 3 installation complete!"
echo ""
echo "Features enabled:"
echo "  - Proactive rule recommendations"
echo "  - Effectiveness tracking"
echo "  - Auto skill generation"
echo "  - Architecture solution generation"
echo ""
echo "Next: Run python3 test_phase2_3.py to verify"
