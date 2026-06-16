# 上传指南

## 准备工作

代码库已准备就绪，位于：`~/opencode-auto-learning/`

### 文件清单

```
opencode-auto-learning/
├── README.md                    # 项目主文档
├── LICENSE                      # MIT License
├── .gitignore                   # Git 忽略文件
├── install.sh                   # 安装脚本
├── docs/
│   ├── ENHANCEMENT_ANALYSIS.md  # 增强功能分析
│   ├── tutorial/
│   │   └── QUICKSTART.md        # 快速入门教程
│   ├── api/
│   │   └── MCP_TOOLS.md         # API 文档
│   └── examples/
│       └── USAGE_EXAMPLES.md    # 使用示例
├── src/
│   ├── mcp/
│   │   ├── mem0_mcp_server.py   # MCP 服务
│   │   └── mem0_wrapper.sh      # 启动脚本
│   ├── learning/
│   │   ├── extractor/
│   │   │   └── memory_extractor.py
│   │   ├── generator/
│   │   │   └── skill_generator.py
│   │   ├── vector/
│   │   │   └── semantic_search.py
│   │   └── graph/
│   │       └── knowledge_graph.py
│   └── bridge/
│       ├── opencode-hermes-bridge.py
│       ├── opencode-bridge.sh
│       └── obsidian-sync.py
├── config/
│   ├── zshrc-addon.sh           # Zsh 配置
│   └── opencode-mcp-config.json # MCP 配置示例
└── scripts/
    └── opencode-auto-learn      # CLI 工具
```

## 上传步骤

### 1. 初始化 Git 仓库

```bash
cd ~/opencode-auto-learning
git init
git add .
git commit -m "Initial commit: OpenCode Auto-Learning System"
```

### 2. 创建 GitHub 仓库

在 GitHub 上创建新仓库：
- 仓库名：`opencode-auto-learning`
- 描述：`🧠 Auto-learning system for OpenCode - semantic search, knowledge graph, skill generation`
- 公开/私有：根据你的选择

### 3. 上传到 GitHub

```bash
# 添加远程仓库
git remote add origin https://github.com/YOUR_USERNAME/opencode-auto-learning.git

# 推送
git push -u origin main
```

### 4. 验证上传

访问 `https://github.com/YOUR_USERNAME/opencode-auto-learning`
确认所有文件已上传。

## 发布 Release

### 创建 Release

1. 在 GitHub 仓库页面点击 "Releases"
2. 点击 "Create a new release"
3. 标签版本：`v1.0.0`
4. 标题：`OpenCode Auto-Learning v1.0.0`
5. 内容：

```markdown
## 🎉 OpenCode Auto-Learning System v1.0.0

### Features
- ✅ Smart memory extraction
- ✅ Auto skill generation
- ✅ Semantic search
- ✅ Knowledge graph
- ✅ Hermes/Obsidian sync
- ✅ MCP integration

### Installation
```bash
git clone https://github.com/YOUR_USERNAME/opencode-auto-learning.git
cd opencode-auto-learning
./install.sh
```

### Documentation
See [docs/tutorial/QUICKSTART.md](docs/tutorial/QUICKSTART.md)

### License
MIT License
```

## 后续迭代

### 分支策略

```bash
# 创建开发分支
git checkout -b develop

# 创建功能分支
git checkout -b feature/active-recommendation

# 合并到开发
git checkout develop
git merge feature/active-recommendation

# 发布
git checkout main
git merge develop
git tag v1.1.0
git push origin main --tags
```

### 迭代计划

根据 [ENHANCEMENT_ANALYSIS.md](ENHANCEMENT_ANALYSIS.md)：

**v1.1.0** - Active Recommendation
- 主动推荐系统
- 上下文感知

**v1.2.0** - Smart Summary
- AI 驱动的总结生成
- 自动报告

**v2.0.0** - Skill Store
- 技能商店
- 社区分享

## 营销建议

### 发布到社区

1. **Reddit**: r/opencode, r/MachineLearning
2. **Twitter**: 分享关键功能
3. **GitHub Topics**: 添加标签 `opencode`, `ai-memory`, `knowledge-graph`
4. **博客文章**: 介绍技术实现

### 宣传文案

**Twitter:**
```
🧠 Just released: OpenCode Auto-Learning System!

Turn your OpenCode into a self-evolving AI assistant:
✅ Auto-extract decisions & learnings
✅ Semantic search your knowledge
✅ Generate skills from patterns
✅ Build knowledge graphs

GitHub: github.com/YOUR_USERNAME/opencode-auto-learning

#OpenCode #AI #Productivity
```

**README 徽章:**
```markdown
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)]()
```

---

**Ready to upload!** 🚀