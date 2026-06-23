# OpenCode Anti-Regression Rules

防套娃规则集 - 为 OpenCode 添加防回归保护机制

## 📋 规则清单

| 规则文件 | 方案来源 | 核心机制 | 触发时机 |
|----------|----------|----------|----------|
| `tdd-enforcement.md` | 方案2 (TDD) | 红绿重构循环 | 代码编写时 |
| `pre-commit-verification.md` | 方案4 (代码审查) | 预提交检查清单 | git commit前 |
| `three-strikes-rule.md` | 方案1 (系统化调试) | 3次失败法则 | 修复失败时 |

## 🎯 防套娃原理

### 1. TDD 强制门控
```
写代码前 → 必须先写测试 → 看测试失败 → 写最小代码 → 看测试通过 → 重构
```
**防止**: 无测试的代码、症状修复、范围失控

### 2. 预提交审查
```
提交前 → 自检清单 → 安全扫描 → 回归测试 → Lint检查 → [verified]提交
```
**防止**: 回归、密钥泄露、调试代码残留

### 3. 3次失败法则
```
第1次失败 → 重新调查
第2次失败 → 深度分析
第3次失败 → STOP，质疑架构
```
**防止**: 无尽套娃、症状修复、架构问题

## 🔧 集成方式

### 方式1: 规则自动注入（推荐）

OpenCode 会自动读取 `~/.config/opencode/rules/*.md` 并注入到每个会话。

**验证规则加载：**
```bash
# 查看规则目录
ls -la ~/.config/opencode/rules/

# 应该看到:
# execution-discipline.md (已有)
# tdd-enforcement.md (新增)
# pre-commit-verification.md (新增)
# three-strikes-rule.md (新增)
```

### 方式2: 项目级 AGENTS.md

在特定项目的 `.opencode/AGENTS.md` 中添加：
```markdown
## Anti-Regression Rules

参考: ~/.config/opencode/rules/tdd-enforcement.md
参考: ~/.config/opencode/rules/pre-commit-verification.md
参考: ~/.config/opencode/rules/three-strikes-rule.md
```

### 方式3: 配置文件中指定

在 `~/.config/opencode/opencode.json` 中添加规则引用：
```json
{
  "rules": [
    "~/.config/opencode/rules/tdd-enforcement.md",
    "~/.config/opencode/rules/pre-commit-verification.md",
    "~/.config/opencode/rules/three-strikes-rule.md"
  ]
}
```

## 📊 效果对比

| 场景 | 无规则 | 有规则 |
|------|--------|--------|
| 修复Bug | 可能引入新Bug | 测试保护，回归检测 |
| 添加功能 | 范围可能失控 | TDD约束，最小化代码 |
| 多次修复失败 | 继续尝试第4、5次... | 第3次失败STOP，质疑架构 |
| 代码质量 | 依赖自觉 | 强制检查清单 |
| 回归风险 | 高 | 低（测试+审查） |

## 🚀 使用示例

### 示例1: 修复Bug（TDD流程）

```
用户: 修复XX功能

OpenCode:
1. [TDD规则触发] 先查找/编写失败测试
2. 运行测试，确认失败
3. 编写最小修复代码
4. 运行测试，确认通过
5. 运行全部测试，确认无回归
6. [预提交规则触发] 自检清单
7. git commit -m "[verified] 修复XX功能"
```

### 示例2: 修复失败（3次失败法则）

```
用户: 修复YY问题

OpenCode:
1. 尝试修复1 → 失败 → 重新调查
2. 尝试修复2 → 失败 → 深度分析
3. 尝试修复3 → 失败 → [3次失败法则触发]

OpenCode:
🛑 ARCHITECTURAL PROBLEM DETECTED
可能不是修复问题，而是架构问题。
建议:
- 重构架构
- 改变方案
- 升级到人工处理
```

### 示例3: 提交代码（预提交审查）

```
OpenCode准备提交:

[预提交规则触发]
✓ 自检清单通过
✓ 安全扫描通过
✓ 回归测试通过 (0 new failures)
✓ Lint检查通过

git commit -m "[verified] 添加ZZ功能"
```

## ⚙️ 自定义配置

### 调整TDD严格程度

编辑 `tdd-enforcement.md`:
```markdown
## 严格级别
- STRICT: 所有代码必须有测试
- RELAXED: 仅核心逻辑需要测试
- MINIMAL: 至少有一个集成测试
```

### 添加项目特定检查

编辑 `pre-commit-verification.md`，在Step 2添加：
```bash
# 项目特定检查
custom-lint.sh || echo "项目检查失败"
```

### 调整失败阈值

编辑 `three-strikes-rule.md`:
```markdown
| Attempt | Action |
|---------|--------|
| 1st fail | 重新调查 |
| 2nd fail | **STOP** (如果偏好更严格) |
```

## 📚 相关技能

这些规则与 Hermes 的以下技能对应：
- `test-driven-development` → `tdd-enforcement.md`
- `requesting-code-review` → `pre-commit-verification.md`
- `systematic-debugging` → `three-strikes-rule.md`

可以在 Hermes 中使用这些技能获得更详细的执行指导。

## ✅ 验证安装

```bash
# 1. 检查规则文件存在
ls -la ~/.config/opencode/rules/*.md

# 2. 检查文件内容
head -5 ~/.config/opencode/rules/tdd-enforcement.md

# 3. 重启 OpenCode（如果需要）
# 规则应该自动生效

# 4. 测试规则
# 尝试让 OpenCode 写代码，观察是否触发TDD规则
```

## 🎉 预期效果

启用这些规则后：
1. ✅ 每个代码修改都有测试保护
2. ✅ 每次提交都经过审查
3. ✅ 修复失败3次自动STOP
4. ✅ 大幅减少回归Bug
5. ✅ 代码质量显著提升
6. ✅ 告别"修复A破坏B"的套娃困境

---

**规则版本**: 1.0.0
**创建时间**: 2026-06-17
**适用**: OpenCode CLI / Desktop
