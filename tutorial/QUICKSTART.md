# 快速入门教程

## 1. 系统概述

OpenCode 自动进化学习系统通过三层架构实现智能学习：

### 三层架构

```
┌─────────────────────────────────────┐
│ Layer 1: 记忆层 (Memory Layer)       │
│  - 自动提取对话中的关键信息          │
│  - 分类存储：决策/学习/错误/模式      │
└─────────────┬───────────────────────┘
              ↓
┌─────────────────────────────────────┐
│ Layer 2: 理解层 (Understanding)      │
│  - 语义搜索：向量嵌入 + 相似度计算    │
│  - 知识图谱：发现记忆间关联          │
└─────────────┬───────────────────────┘
              ↓
┌─────────────────────────────────────┐
│ Layer 3: 应用层 (Application)        │
│  - 技能生成：从重复模式生成技能      │
│  - 主动推荐：预测需要的上下文        │
│  - 自动同步：Hermes/Obsidian 归档   │
└─────────────────────────────────────┘
```

## 2. 安装步骤

### 步骤 1: 克隆仓库

```bash
git clone https://github.com/yourusername/opencode-auto-learning.git
cd opencode-auto-learning
```

### 步骤 2: 运行安装脚本

```bash
# 自动安装所有组件
./install.sh

# 或手动安装
./install.sh --manual
```

### 步骤 3: 配置环境

安装脚本会自动添加配置到 `~/.zshrc`，你也可以手动配置：

```bash
# 添加到你的 ~/.zshrc
source ~/.opencode-auto-learning/zshrc-addon.sh
```

### 步骤 4: 重启终端

```bash
source ~/.zshrc
```

## 3. 基础使用

### 3.1 启动带自动学习的 OpenCode

```bash
# 使用增强版启动命令
oc-learn /path/to/your/project

# 正常退出后，系统会自动：
# 1. 提取会话中的记忆
# 2. 生成技能（如果有重复模式）
# 3. 同步到 Hermes/Obsidian
```

### 3.2 手动触发学习

```bash
# 运行完整学习流程
opencode-auto-learn run

# 输出示例：
# 📚 Phase 1: Extracting memories...
#    Extracted 5 memories
# 🔨 Phase 2: Generating skills...
#    Generated 2 skills
# 🔄 Phase 3: Syncing to Hermes...
#    Synced 5 memories
# 📓 Phase 4: Syncing to Obsidian...
#    Synced to Daily Sync/2026-06-16.md
```

### 3.3 查看状态

```bash
# 查看系统状态
opencode-auto-learn status

# 输出示例：
# 📊 Learning System Status
#   Memories:      42
#   Auto-skills:   8
#   Scheduled sync: ✅ Running
```

## 4. 进阶功能

### 4.1 语义搜索

```bash
# 搜索与"deployment"相关的记忆
opencode-auto-learn semantic-search "deployment"

# 输出示例：
# 🔍 Search results for: deployment
#   [95.3%] DevOps: 决定使用 Docker Compose 部署服务...
#   [87.1%] technical: Kubernetes deployment 配置...
#   [82.5%] learning: 学习到蓝绿部署模式...
```

### 4.2 知识图谱

```bash
# 构建知识图谱
opencode-auto-learn build-graph

# 输出示例：
# 🕸️ Building knowledge graph...
# ✅ Built graph: 42 nodes, 156 edges

# 查看知识聚类
opencode-auto-learn clusters

# 输出示例：
# 📊 Top clusters:
#   - deployment: 8 nodes
#   - kubernetes: 5 nodes
#   - monitoring: 4 nodes
```

### 4.3 查找关联记忆

```bash
# 查找与特定记忆相关的其他记忆
opencode-auto-learn related "docker-compose-setup"

# 输出示例：
# 🔍 Memories related to docker-compose-setup:
#   Direct: 3 connections
#     - nginx-config: same_category (0.8)
#     - ssl-setup: keyword_overlap (0.7)
#     - load-balancer: temporal_proximity (0.6)
```

## 5. MCP 工具使用

在 OpenCode 对话中，你可以直接使用 MCP 工具：

### 5.1 召回上下文

```
User: 帮我 recall 关于 deployment 的记忆

Assistant: 使用 MCP 工具 mem0-memory/recall_context
→ 返回相关记忆列表
```

### 5.2 语义搜索

```
User: 搜索与 "性能优化" 相关的所有内容

Assistant: 使用 MCP 工具 mem0-memory/semantic_search
→ 按相似度排序返回结果
```

### 5.3 保存记忆

```
User: 记住这个决定：我们使用 PostgreSQL 而不是 MySQL

Assistant: 使用 MCP 工具 mem0-memory/save_memory
→ 自动分类为 "decision"
```

### 5.4 获取知识聚类

```
User: 分析我的知识图谱，有什么聚类？

Assistant: 使用 MCP 工具 mem0-memory/get_clusters
→ 返回关键词聚类分析
```

## 6. 工作流配置

### 6.1 定时学习

编辑 `~/.config/opencode/workflows/auto-learning.yaml`：

```yaml
triggers:
  - type: scheduled
    schedule: "0 */6 * * *"  # 每6小时
```

### 6.2 自定义记忆类型

编辑 `~/.config/opencode/memory/config/memory-types.json`：

```json
{
  "my_custom_type": {
    "description": "Custom memory type",
    "icon": "🎯",
    "priority": "high",
    "autoExtract": true
  }
}
```

## 7. 故障排除

### 问题 1: MCP 服务显示红色 OFF

**解决方案：**
```bash
# 检查权限
chmod +x ~/.config/opencode/mcp-servers/*.sh
chmod +x ~/.config/opencode/mcp-servers/*.py

# 测试服务
echo '{"tool":"get_categories"}' | ~/.config/opencode/mcp-servers/mem0_wrapper.sh

# 重启 OpenCode
pkill -f "OpenCode" && open "/Applications/OpenCode Dev.app"
```

### 问题 2: 语义搜索返回空结果

**解决方案：**
```bash
# 重新构建索引
python3 ~/.config/opencode/skills/auto-learning/vector/semantic_search.py build

# 检查数据库
ls -la ~/.mem0/vector_memory.db
```

### 问题 3: 知识图谱为空

**解决方案：**
```bash
# 确保有记忆文件
ls ~/.config/opencode/memory/user/*.md

# 重新构建图谱
python3 ~/.config/opencode/skills/auto-learning/graph/knowledge_graph.py build
```

## 8. 最佳实践

### 8.1 记忆管理

- **定期回顾**：每周运行 `opencode-auto-learn status` 查看记忆增长
- **手动标记**：重要决策使用 `#decision` 标签
- **分类整理**：利用知识图谱发现知识缺口

### 8.2 技能优化

- **审查生成的技能**：检查 `~/.config/opencode/skills/auto-generated/`
- **命名规范**：手动技能放在 `~/.config/opencode/skills/my-skills/`
- **版本控制**：技能变更提交到 Git

### 8.3 同步策略

- **开发时**：使用 `oc-learn` 自动同步
- **结束时**：手动运行 `opencode-auto-learn run` 确保同步
- **定期备份**：Obsidian Vault 定期 Git 提交

## 9. 下一步

- [API Reference](api/MCP_TOOLS.md) - 完整的 MCP 工具文档
- [Examples](examples/USAGE_EXAMPLES.md) - 更多使用示例
- [Architecture](ARCHITECTURE.md) - 系统架构详解

---

**恭喜！你现在拥有完整的 OpenCode 自动进化学习系统！** 🎉
