# OpenCode Auto Learning System

从 OpenCode 会话自动提取记忆并生成技能的完整系统。

## 功能特性

- **会话导出**: 从 OpenCode 数据库导出会话为 Markdown
- **智能提取**: 自动识别代码、决策、错误解决方案等知识点
- **技能生成**: 将记忆转换为结构化技能文件
- **分类管理**: 按类型自动分类（命令、代码、配置、决策、错误）

## 快速开始

```bash
# 运行完整流程
./scripts/opencode_learning/opencode-learn

# 单独步骤
./scripts/opencode_learning/opencode-learn export    # 导出会话
./scripts/opencode_learning/opencode-learning extract   # 提取记忆
./scripts/opencode_learning/opencode-learning generate  # 生成技能
./scripts/opencode_learning/opencode-learning status    # 查看状态
```

## 系统架构

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Export    │────▶│   Extract   │────▶│   Generate  │
│  Sessions   │     │  Memories   │     │   Skills    │
└─────────────┘     └─────────────┘     └─────────────┘
       │                    │                    │
       ▼                    ▼                    ▼
~/.config/opencode/   ~/.config/opencode/   ~/.config/opencode/
  memory/sessions/      memory/user/         skills/auto-generated/
```

## 文件说明

| 文件 | 说明 |
|------|------|
| `export_sessions.py` | 从 SQLite 导出会话 |
| `extract_memories.py` | 智能提取知识点 |
| `generate_skills.py` | 生成技能文件 |
| `opencode-learn` | 统一工作流入口 |

## 生成的技能类型

- **auto-commands**: 常用 Shell 命令
- **auto-code-snippets**: 代码片段参考
- **auto-configs**: 配置模式
- **auto-decisions**: 技术决策记录
- **auto-errors**: 错误解决方案

## 依赖

- Python 3.8+
- OpenCode 数据库 (~/.local/share/opencode/opencode-.db)

## 许可证

MIT
