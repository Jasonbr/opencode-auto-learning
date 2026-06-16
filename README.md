# 🧠 OpenCode 自动进化学习系统

完整的学习系统，让 OpenCode 像 Hermes 一样自动进化。

## 🎯 功能特性

- ✅ **智能记忆提取** - 自动识别决策、学习、错误解决
- ✅ **技能自动生成** - 从重复模式生成可复用技能
- ✅ **语义搜索** - 向量嵌入，语义相似度搜索
- ✅ **知识图谱** - 记忆关联网络，发现隐性知识
- ✅ **自动同步** - Hermes/Obsidian 双向同步
- ✅ **MCP 集成** - 通过 MCP 协议与 OpenCode 深度集成

## 📦 快速开始

### 安装

```bash
# 克隆仓库
git clone https://github.com/Jasonbr/opencode-auto-learning.git
cd opencode-auto-learning

# 运行安装脚本
./install.sh
```

### 配置

```bash
# 添加到 .zshrc
echo 'source ~/.opencode-auto-learning/zshrc-addon.sh' >> ~/.zshrc
source ~/.zshrc
```

### 使用

```bash
# 启动 OpenCode（带自动学习）
oc-learn /path/to/project

# 手动触发学习
opencode-auto-learn run

# 语义搜索
opencode-auto-learn semantic-search "deployment"

# 查看知识图谱
opencode-auto-learn build-graph
```

## 📚 文档

- [Tutorial](tutorial/QUICKSTART.md) - 快速入门教程
- [API Reference](api/MCP_TOOLS.md) - MCP 工具 API 文档
- [Examples](examples/USAGE_EXAMPLES.md) - 使用示例

## 🏗️ 架构

```
OpenCode
  ↓ MCP
Mem0 MCP Server
  ├─ Memory Extractor
  ├─ Skill Generator
  ├─ Semantic Search
  └─ Knowledge Graph
  ↓
Hermes / Obsidian
```

## 📄 License

MIT License - see [LICENSE](LICENSE)

## 新功能 (v1.1.0)

### Phase 4: 主动推荐系统
- 上下文分析（关键词/意图/实体）
- 多维度推荐（关键词+意图匹配）
- 命令: `opencode-auto-learn-recommend <text>`

### Phase 5: 智能总结生成
- 多维度总结（决策/学习/行动项）
- 多格式输出（Markdown/JSON/Text）
- 命令: `opencode-summary [daily|weekly|export]`

