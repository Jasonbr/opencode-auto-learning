#!/bin/bash
# OpenCode 自动学习系统安装脚本
# Install OpenCode Auto Learning System

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_DIR="$HOME/.config/opencode"
BIN_DIR="$HOME/bin"

# 颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}================================${NC}"
echo -e "${GREEN}OpenCode 自动学习系统安装器${NC}"
echo -e "${GREEN}================================${NC}"
echo

# 检查 Python
echo "🔍 检查 Python 环境..."
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python3 未安装${NC}"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
REQUIRED_VERSION="3.10"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    echo -e "${YELLOW}⚠️  Python 版本 $PYTHON_VERSION，建议 >= 3.10${NC}"
else
    echo -e "${GREEN}✅ Python $PYTHON_VERSION${NC}"
fi

# 检查目录
echo
echo "📁 创建目录结构..."
mkdir -p "$CONFIG_DIR/skills/auto-learning"/{extractor,generator,graph,vector,multimodal,recommender,summarizer}
mkdir -p "$CONFIG_DIR/memory"/{user,sessions,config,obsidian-sync,project}
mkdir -p "$CONFIG_DIR/mcp-servers"
mkdir -p "$CONFIG_DIR/rules"
mkdir -p "$BIN_DIR"
echo -e "${GREEN}✅ 目录创建完成${NC}"

# 复制文件
echo
echo "📦 复制文件..."

# 核心组件
cp -r "$SCRIPT_DIR/src/extractor"/* "$CONFIG_DIR/skills/auto-learning/extractor/"
cp -r "$SCRIPT_DIR/src/generator"/* "$CONFIG_DIR/skills/auto-learning/generator/"
cp -r "$SCRIPT_DIR/src/mcp"/* "$CONFIG_DIR/mcp-servers/"

# 可选组件（如果存在）
for dir in graph vector multimodal recommender summarizer; do
    if [ -d "$SCRIPT_DIR/src/$dir" ]; then
        cp -r "$SCRIPT_DIR/src/$dir"/* "$CONFIG_DIR/skills/auto-learning/$dir/" 2>/dev/null || true
    fi
done

# 脚本
cp "$SCRIPT_DIR/src/scripts/opencode-auto-learn" "$BIN_DIR/"
cp "$SCRIPT_DIR/src/scripts/opencode-export-sessions" "$BIN_DIR/"
cp "$SCRIPT_DIR/src/scripts/opencode-export-sessions-v2" "$BIN_DIR/"
cp "$SCRIPT_DIR/src/scripts/opencode-extract-memories" "$BIN_DIR/"
cp "$SCRIPT_DIR/src/scripts/opencode-generate-skills-v3" "$BIN_DIR/"
cp "$SCRIPT_DIR/src/scripts/opencode-bridge.sh" "$BIN_DIR/"

# 规则
cp "$SCRIPT_DIR/rules"/*.md "$CONFIG_DIR/rules/" 2>/dev/null || true

# 设置权限
chmod +x "$BIN_DIR"/opencode-*
chmod +x "$CONFIG_DIR/mcp-servers/mem0_wrapper.sh"

echo -e "${GREEN}✅ 文件复制完成${NC}"

# 创建 SKILL.md
echo
echo "📝 创建 SKILL.md..."
cat > "$CONFIG_DIR/skills/auto-learning/SKILL.md" << 'EOF'
---
name: auto-learning
title: OpenCode Auto Learning System
description: 自动化记忆提取和技能生成系统
tags: [opencode, auto-learning, memory, skill-generation, mcp]
---

# Auto Learning Skill

自动化记忆提取和技能生成系统。

## 功能

- **记忆提取**：从会话中提取学习、决策、错误、配置、命令等 5 类记忆
- **技能生成**：基于记忆自动生成可复用的 skill
- **知识图谱**：构建记忆之间的关系网络
- **会话摘要**：生成每日学习摘要

## 使用方式

### 手动运行

```bash
# 完整流程
~/bin/opencode-auto-learn full

# 单独步骤
~/bin/opencode-auto-learn export      # 导出会话
~/bin/opencode-auto-learn extract     # 提取记忆
~/bin/opencode-auto-learn generate    # 生成技能
~/bin/opencode-auto-learn sync        # 同步到 Hermes

# 查看状态
~/bin/opencode-auto-learn status
```

### 自动运行

通过 LaunchAgent 每天凌晨 3:00 自动运行。

## 存储位置

- **记忆文件**：`~/.config/opencode/memory/user/`
- **生成技能**：`~/.config/opencode/skills/auto-generated/`
- **会话文件**：`~/.config/opencode/memory/sessions/`

## 子模块

- `extractor/`：记忆提取器
- `generator/`：技能生成器
- `graph/`：知识图谱
- `multimodal/`：多模态支持
- `recommender/`：技能推荐
- `summarizer/`：会话摘要
- `vector/`：向量存储
EOF

echo -e "${GREEN}✅ SKILL.md 创建完成${NC}"

# 配置 MCP Server
echo
echo "🔌 配置 MCP Server..."
CONFIG_FILE="$CONFIG_DIR/opencode.json"

if [ -f "$CONFIG_FILE" ]; then
    echo -e "${YELLOW}⚠️  检测到现有配置，添加 MCP 配置...${NC}"
    # 备份
    cp "$CONFIG_FILE" "$CONFIG_FILE.backup.$(date +%Y%m%d%H%M%S)"
    
    # 注意：这里需要手动合并 JSON
    echo -e "${YELLOW}请手动在 $CONFIG_FILE 中添加以下配置:${NC}"
    cat << 'EOF'
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
EOF
else
    echo -e "${YELLOW}⚠️  未检测到 OpenCode 配置，请手动配置 MCP${NC}"
fi

# 配置 LaunchAgent (macOS)
echo
echo "⏰ 配置自动运行..."
LAUNCHD_DIR="$HOME/Library/LaunchAgents"
mkdir -p "$LAUNCHD_DIR"

PLIST_FILE="$LAUNCHD_DIR/com.opencode.auto-learning.plist"

cat > "$PLIST_FILE" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.opencode.auto-learning</string>
    <key>ProgramArguments</key>
    <array>
        <string>$BIN_DIR/opencode-auto-learn</string>
        <string>full</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>3</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>
    <key>StandardOutPath</key>
    <string>$CONFIG_DIR/memory/auto-learning.log</string>
    <key>StandardErrorPath</key>
    <string>$CONFIG_DIR/memory/auto-learning-error.log</string>
</dict>
</plist>
EOF

# 加载 LaunchAgent
launchctl load "$PLIST_FILE" 2>/dev/null || true

echo -e "${GREEN}✅ LaunchAgent 配置完成${NC}"
echo "   每天凌晨 3:00 自动运行"

# 验证安装
echo
echo "🔍 验证安装..."
echo "================================"

# 检查脚本
echo -n "主脚本: "
if [ -x "$BIN_DIR/opencode-auto-learn" ]; then
    echo -e "${GREEN}✅${NC}"
else
    echo -e "${RED}❌${NC}"
fi

# 检查组件
echo -n "记忆提取器: "
if [ -f "$CONFIG_DIR/skills/auto-learning/extractor/memory_extractor.py" ]; then
    echo -e "${GREEN}✅${NC}"
else
    echo -e "${RED}❌${NC}"
fi

echo -n "技能生成器: "
if [ -f "$CONFIG_DIR/skills/auto-learning/generator/skill_generator.py" ]; then
    echo -e "${GREEN}✅${NC}"
else
    echo -e "${RED}❌${NC}"
fi

echo -n "MCP Server: "
if [ -f "$CONFIG_DIR/mcp-servers/mem0_mcp_server.py" ]; then
    echo -e "${GREEN}✅${NC}"
else
    echo -e "${RED}❌${NC}"
fi

# 检查规则
echo -n "AI 规则: "
RULE_COUNT=$(ls "$CONFIG_DIR/rules"/*.md 2>/dev/null | wc -l)
if [ "$RULE_COUNT" -gt 0 ]; then
    echo -e "${GREEN}✅ ($RULE_COUNT 个)${NC}"
else
    echo -e "${YELLOW}⚠️ (0 个)${NC}"
fi

echo
echo "================================"
echo -e "${GREEN}✅ 安装完成!${NC}"
echo
echo "使用方法:"
echo "  opencode-auto-learn status    # 查看状态"
echo "  opencode-auto-learn full      # 运行完整流程"
echo
echo "文档:"
echo "  README.md - 项目说明"
echo "  CHANGELOG.md - 更新日志"
echo
echo "⚠️  注意: 请手动在 ~/.config/opencode/opencode.json 中添加 MCP 配置"
