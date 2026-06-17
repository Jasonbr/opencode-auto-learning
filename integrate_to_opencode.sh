#!/bin/bash
# 将防套娃规则集成到 OpenCode

echo "🔧 Integrating Anti-Regression Rules into OpenCode..."

# 1. 备份当前配置
if [ -f ~/.config/opencode/opencode.json ]; then
    cp ~/.config/opencode/opencode.json ~/.config/opencode/opencode.json.backup.$(date +%Y%m%d_%H%M%S)
    echo "✅ Backup created"
fi

# 2. 创建 Python 启动脚本
mkdir -p ~/.config/opencode/scripts

cat > ~/.config/opencode/scripts/activate_rules.py << 'PYTHON'
"""
OpenCode 规则激活脚本
在 OpenCode 启动时自动加载防套娃规则
"""

import sys
import os

# 添加规则集成路径
sys.path.insert(0, os.path.expanduser('~/opencode-auto-learning/src'))

try:
    from rules_integration import (
        RuleTracker,
        RuleRecommender,
        ArchitectureSolutionGenerator
    )
    
    # 创建全局 tracker 实例
    rule_tracker = RuleTracker()
    rule_recommender = RuleRecommender()
    arch_generator = ArchitectureSolutionGenerator()
    
    print("✅ Anti-regression rules loaded successfully")
    print(f"   - RuleTracker: Active")
    print(f"   - RuleRecommender: Active")
    print(f"   - ArchitectureSolutionGenerator: Active")
    
except Exception as e:
    print(f"⚠️  Rules integration not loaded: {e}")
    print("   Run: cd ~/opencode-auto-learning && ./install_phase1.sh")

PYTHON

echo "✅ Python activation script created"

# 3. 创建 OpenCode 钩子脚本（如果支持）
if [ -d ~/.config/opencode/.sisyphus ]; then
    cat > ~/.config/opencode/.sisyphus/rules_hook.js << 'JS'
// Sisyphus 钩子 - 在代码编辑前执行
const { execSync } = require('child_process');

module.exports = {
  beforeEdit: (context) => {
    // 运行规则推荐
    try {
      execSync('python3 ~/.config/opencode/scripts/activate_rules.py', { stdio: 'inherit' });
    } catch (e) {
      // 静默失败，不阻塞编辑
    }
  }
};
JS
    echo "✅ Sisyphus hook created"
fi

# 4. 创建命令别名
cat >> ~/.zshrc << 'ALIAS'

# OpenCode with Anti-Regression Rules
alias oc-rules='python3 ~/.config/opencode/scripts/activate_rules.py && opencode'
alias oc-learn='cd ~/opencode-auto-learning && ./install_phase1.sh 2>/dev/null; opencode'

ALIAS

echo "✅ Aliases added to ~/.zshrc"

# 5. 创建状态检查脚本
cat > ~/.config/opencode/scripts/check_rules_status.py << 'CHECK'
#!/usr/bin/env python3
"""检查规则集成状态"""

import sys
import os

sys.path.insert(0, os.path.expanduser('~/opencode-auto-learning/src'))

print("=" * 60)
print("OpenCode Anti-Regression Rules Status")
print("=" * 60)

# 检查模块
modules = [
    ('rules_integration.rule_tracker', 'RuleTracker'),
    ('rules_integration.rule_recommender', 'RuleRecommender'),
    ('rules_integration.architecture_generator', 'ArchitectureSolutionGenerator'),
]

all_loaded = True
for module_name, class_name in modules:
    try:
        module = __import__(module_name, fromlist=[class_name])
        getattr(module, class_name)
        print(f"✅ {class_name:30s} Loaded")
    except Exception as e:
        print(f"❌ {class_name:30s} Not loaded: {e}")
        all_loaded = False

print("=" * 60)
if all_loaded:
    print("🎉 All modules loaded successfully!")
    print("\nUsage:")
    print("  from rules_integration import RuleTracker")
    print("  tracker = RuleTracker()")
    print("  tracker.track_tdd_execution({...})")
else:
    print("⚠️  Some modules not loaded")
    print("\nTo install:")
    print("  cd ~/opencode-auto-learning")
    print("  ./install_phase1.sh")
    print("  ./install_phase2_3.sh")
print("=" * 60)
CHECK

chmod +x ~/.config/opencode/scripts/check_rules_status.py

echo "✅ Status check script created"

# 6. 运行状态检查
python3 ~/.config/opencode/scripts/check_rules_status.py

echo ""
echo "🎉 Integration complete!"
echo ""
echo "Next steps:"
echo "  1. Reload shell: source ~/.zshrc"
echo "  2. Use 'oc-rules' to start OpenCode with rules"
echo "  3. Run 'python3 ~/.config/opencode/scripts/check_rules_status.py' to verify"
echo ""
echo "Or manually integrate in Python:"
echo "  import sys"
echo "  sys.path.insert(0, '~/opencode-auto-learning/src')"
echo "  from rules_integration import RuleTracker"
