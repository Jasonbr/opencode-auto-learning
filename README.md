# OpenCode Auto Learning System

🧠 **OpenCode 自动学习系统** - 让 OpenCode 像 Hermes Agent 一样自动进化

为 OpenCode 实现自动记忆提取、技能生成和知识积累，类似 Hermes 的 fact_store 和技能系统。

## ✨ 核心功能

| 功能 | 描述 | 状态 |
|------|------|------|
| 🧠 **记忆提取** | 从会话中自动提取 5 类记忆 (决策/学习/错误/配置/命令) | ✅ 运行中 |
| 🔨 **技能生成** | 基于记忆模式自动生成可复用 Skill | ✅ 运行中 |
| 🌐 **知识图谱** | 构建记忆之间的关联网络 | ✅ 已部署 |
| 🔍 **语义搜索** | 向量检索历史记忆 | ✅ 已部署 |
| 📝 **会话摘要** | 自动生成每日学习摘要 | ✅ 已部署 |
| 🔄 **Hermes 桥接** | 双向同步记忆到 Hermes + Obsidian | ✅ 运行中 |
| 🔌 **MCP 集成** | 通过 MCP Server 与 OpenCode 深度集成 | ✅ 已连接 |

## 📊 运行数据

```
🧠 提取记忆: 1,297 条
📁 会话文件: 42 个
🔨 生成技能: 5 个分类
🔄 同步状态: 正常运行
```

## 🚀 快速开始


### 安装

```bash
# 1. 克隆仓库
git clone https://github.com/YOUR_USERNAME/opencode-auto-learning.git
cd opencode-auto-learning

# 2. 运行安装脚本
./install.sh

# 3. 验证安装
opencode-auto-learn status
```

### 使用

```bash
# 运行完整流程
opencode-auto-learn

# 单独步骤
opencode-auto-learn export      # 导出最新会话
opencode-auto-learn extract     # 提取记忆
opencode-auto-learn generate    # 生成技能
opencode-auto-learn sync        # 同步到 Hermes

# 查看状态
opencode-auto-learn status
```

### 自动运行

系统通过 macOS LaunchAgent 每天凌晨 3:00 自动运行：

```bash
# 检查状态
launchctl list | grep com.opencode.auto-learning

# 手动触发
launchctl start com.opencode.auto-learning
```

## 📁 项目结构

```
opencode-auto-learning/
├── README.md                    # 本文件
├── CHANGELOG.md               # 版本历史
├── LICENSE                    # MIT 许可证
├── install.sh                 # 安装脚本
├── docs/                    # 文档
│   ├── ARCHITECTURE.md      # 架构说明
│   ├── API.md               # API 文档
│   └── TROUBLESHOOTING.md   # 故障排除
├── src/                     # 源代码
│   ├── extractor/           # 记忆提取器
│   │   └── memory_extractor.py
│   ├── generator/           # 技能生成器
│   │   └── skill_generator.py
│   ├── mcp/                 # MCP Server
│   │   ├── mem0_mcp_server.py
│   │   ├── enhanced_memory.py
│   │   └── mem0_wrapper.sh
│   ├── bridge/              # Hermes 桥接
│   │   └── opencode_bridge.sh
│   ├── graph/               # 知识图谱
│   ├── vector/              # 向量搜索
│   └── scripts/             # CLI 脚本
│       ├── opencode-auto-learn
│       ├── opencode-export-sessions
│       ├── opencode-extract-memories
│       └── opencode-generate-skills-v3
├── rules/                   # AI 编码规则
│   ├── tdd-enforcement.md
│   ├── three-strikes-rule.md
│   ├── pre-commit-verification.md
│   └── execution-discipline.md
└── config/                  # 配置文件
    └── opencode.json.example
```

## 🔧 系统架构

```
OpenCode 会话
    ↓
[导出器] → 会话 Markdown 文件
    ↓
[提取器] → 分类记忆 (decision/learning/error/config/command)
    ↓
[生成器] → 自动生成 Skill
    ↓
[桥接器] → 同步到 Hermes + Obsidian
    ↓
[MCP Server] → OpenCode 实时调用
```

## 🔌 MCP Server 配置

在 `~/.config/opencode/opencode.json` 中添加：

```json
{
  "mcp": {
    "mem0-memory": {
      "type": "local",
      "command": [
        "sh",
        "~/.config/opencode/mcp-servers/mem0_wrapper.sh"
      ],
      "timeout": 30000
    }
  }
}
```

验证连接：
```bash
opencode mcp list
```

## 📜 AI 编码规则

项目包含 4 个核心编码规则，可显著提升代码质量：

1. **TDD 强制规则** - 强制先写测试再写实现
2. **Three-Strikes 规则** - 3次修复失败后停止并重新审视架构
3. **预提交验证** - 提交前自动安全检查
4. **执行纪律** - 强制执行计划审批流程

规则文件位置：`~/.config/opencode/rules/`

## 🤝 与 Hermes 集成

本系统可与 Hermes Agent 双向同步：

```
OpenCode ←→ Hermes Agent
    ↕
Obsidian Vault
```

- OpenCode 提取的记忆同步到 Hermes
- Hermes 的 fact_store 同步到 OpenCode
- 统一归档到 Obsidian 知识库

## 🛠️ 故障排除

### MCP Server 启动失败

```bash
# 检查 Python 环境
python3 --version

# 检查依赖
python3 -c "import sqlite3; print('OK')"

# 手动启动测试
python3 ~/.config/opencode/mcp-servers/mem0_mcp_server.py
```

### 自动学习未运行

```bash
# 检查 LaunchAgent
launchctl list | grep opencode

# 查看日志
cat ~/.config/opencode/memory/sync.log
tail -f ~/.config/opencode/memory/sync-error.log
```

### 技能生成失败

```bash
# 检查记忆目录
ls ~/.config/opencode/memory/user/

# 手动运行生成器
python3 ~/.config/opencode/skills/auto-learning/generator/skill_generator.py
```

## 📈 性能指标

基于实际运行数据：

| 指标 | 数值 |
|------|------|
| 记忆提取成功率 | > 95% |
| 技能生成准确率 | > 80% |
| 每日自动处理 | ~50 条记忆 |
| MCP 响应时间 | < 500ms |

## 📝 更新日志

见 [CHANGELOG.md](./CHANGELOG.md)

## 📄 许可证

MIT License - 详见 [LICENSE](./LICENSE)

## 🙏 致谢

- 灵感来源于 Hermes Agent 的记忆系统
- OpenCode 团队提供的 MCP 协议支持
- Mem0 项目的向量存储架构

---

**注意**：OpenCode 1.15.7 不支持顶层 `"rules"` 键，规则文件需通过其他方式加载（如 oh-my-openagent 插件）。
