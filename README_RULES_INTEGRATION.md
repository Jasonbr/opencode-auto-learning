# OpenCode 防套娃智能系统

AI Coding Anti-Regression System - 防止"修复一个问题却引入新问题"的套娃困境

## 🎯 项目目标

构建一个完整的三阶段智能系统，为 OpenCode 和 oh-my-openagent 提供：

1. **规则执行跟踪** - 自动记录规则执行到学习系统
2. **主动智能推荐** - 在操作前主动推荐相关规则
3. **智能技能生成** - 从成功案例自动生成技能和架构方案

## 🏗️ 系统架构

```
┌─────────────────────────────────────────────────────────────┐
│                    防套娃智能系统 v1.0                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Phase 1: 规则-学习集成 (Rule-Learning Integration)        │
│  ├─ RuleTracker          跟踪规则执行 → Mem0 + KG         │
│  └─ ViolationAnalyzer    分析违规模式 → 提取最佳实践       │
│                                                             │
│  Phase 2: 主动智能推荐 (Proactive Intelligence)            │
│  ├─ RuleRecommender      操作前主动推荐相关规则             │
│  └─ EffectivenessTracker 计算 auto-apply 分数              │
│                                                             │
│  Phase 3: 智能技能生成 (Smart Skill Generation)            │
│  ├─ RuleBasedSkillGenerator  从成功案例自动生成技能      │
│  └─ ArchitectureSolutionGenerator 自动生成架构解决方案   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## 📦 安装

### 快速安装

```bash
# 1. 克隆仓库
git clone https://github.com/Jasonbr/opencode-auto-learning.git
cd opencode-auto-learning

# 2. 安装 Phase 1
./install_phase1.sh

# 3. 安装 Phase 2 & 3
./install_phase2_3.sh
```

### 手动安装

```bash
pip3 install mem0ai networkx

# 复制到 Python 路径
export PYTHONPATH="$PYTHONPATH:$(pwd)/src"
```

## 🚀 快速使用

### Phase 1: 规则执行跟踪

```python
from rules_integration import RuleTracker

# 创建跟踪器
tracker = RuleTracker()

# 跟踪 TDD 执行
tracker.track_tdd_execution({
    "project": "my-project",
    "file": "src/example.py",
    "test_written_first": True,
    "test_failed_first": True,
    "implementation_minimal": True,
    "all_tests_pass": True
})

# 查看统计
stats = tracker.get_execution_stats()
print(f"Success rate: {stats['success_rate']:.1%}")
```

### Phase 2: 主动智能推荐

```python
from rules_integration import RuleRecommender

# 创建推荐器
recommender = RuleRecommender()

# 编辑前推荐
recs = recommender.recommend_before_edit("src/example.py", "edit")
for r in recs:
    print(f"推荐: {r['rule']} (weight={r['weight']:.2f})")
    if r['auto_apply']:
        print("  → 自动应用推荐")

# 提交前推荐
recs = recommender.recommend_before_commit(["src/a.py", "test_b.py"])
```

### Phase 3: 智能技能生成

```python
from rules_integration import (
    RuleBasedSkillGenerator,
    ArchitectureSolutionGenerator
)

# 从成功案例生成技能
generator = RuleBasedSkillGenerator()
skills = generator.generate_all_skills()

# 生成架构解决方案
arch_gen = ArchitectureSolutionGenerator()
solution = arch_gen.generate_from_three_strikes({
    "attempt": 3,
    "fix_description": "Fixed A, broke B...",
    "error_message": "Circular dependency"
})

print(f"解决方案: {solution['title']}")
print(f"步骤数: {len(solution['steps'])}")
print(f"预计时间: {solution['estimated_time']}")
```

## 📊 效果预期

| 指标 | 优化前 | 优化后 | 提升 |
|------|--------|--------|------|
| 规则遵守率 | 60% | 90% | +50% |
| Bug回归率 | ~30% | <5% | -83% |
| 修复成功率 | ~60% | >90% | +50% |
| 知识复用率 | 30% | 70% | +133% |
| 主动推荐覆盖率 | 0% | 85% | +∞ |

## 📁 项目结构

```
opencode-auto-learning/
├── src/rules_integration/          # 核心模块
│   ├── __init__.py
│   ├── rule_tracker.py            # Phase 1
│   ├── violation_analyzer.py      # Phase 1
│   ├── rule_recommender.py        # Phase 2
│   ├── effectiveness_tracker.py   # Phase 2
│   ├── skill_generator.py         # Phase 3
│   └── architecture_generator.py  # Phase 3
├── test_phase1.py                 # Phase 1 测试
├── test_phase2_3.py              # Phase 2+3 测试
├── install_phase1.sh             # Phase 1 安装
└── install_phase2_3.sh           # Phase 2+3 安装

ai-coding-rules/                    # 规则定义
├── opencode-rules/
├── oh-my-openagent-rules/
└── examples/integration/
```

## 🔗 相关仓库

- [opencode-auto-learning](https://github.com/Jasonbr/opencode-auto-learning) - 自动学习系统
- [ai-coding-rules](https://github.com/Jasonbr/ai-coding-rules) - 防套娃规则集

## 📚 文档

- [OPTIMIZATION_PLAN.md](ai-coding-rules/OPTIMIZATION_PLAN.md) - 完整优化方案
- [test_phase1.py](test_phase1.py) - Phase 1 测试
- [test_phase2_3.py](test_phase2_3.py) - Phase 2+3 测试

## 🧪 测试

```bash
# 运行全部测试
python3 test_phase1.py
python3 test_phase2_3.py

# 或者使用 pytest
pytest test_*.py -v
```

## 🤝 贡献

欢迎贡献代码、报告问题或提出改进建议！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m '[verified] Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 📄 许可证

[MIT](LICENSE)

---

**🎉 现在你的 OpenCode 拥有了完整的防套娃 + 自动学习一体化能力！**