# 使用示例

## 示例 1: 开发工作流

### 场景
在开发新功能时，自动保存决策和学到的知识。

### 对话
```
User: 帮我实现一个用户认证系统

Assistant: [实现代码...]

User: 决定使用 JWT 而不是 Session

Assistant: 使用 MCP 工具 mem0-memory/save_memory
→ 自动保存为 "decision" 类型

User: 学习到 JWT 的过期时间应该设置多久？

Assistant: [解释...]
→ 自动提取为 "learning" 类型
```

### 结果
退出 OpenCode 后：
```
✅ Auto-learning completed:
   - 2 memories extracted
   - 1 skill generated (jwt-auth)
   - Synced to Hermes/Obsidian
```

## 示例 2: 故障排查

### 场景
遇到问题时搜索类似的历史解决方案。

### 对话
```
User: 搜索关于 "数据库连接超时" 的解决方案

Assistant: 使用 MCP 工具 mem0-memory/semantic_search
→ 返回：
   [94.2%] error-solution: 解决 PostgreSQL 连接超时...
   [87.5%] technical: 数据库连接池配置...
   
User: 这是什么原理？

Assistant: 根据记忆，这是因为...
```

## 示例 3: 知识发现

### 场景
分析自己的知识体系，发现薄弱环节。

### 命令行
```bash
# 构建知识图谱
opencode-auto-learn build-graph

# 查看聚类
opencode-auto-learn clusters

# 输出：
📊 Knowledge clusters:
   - deployment: 12 nodes (expert)
   - api-design: 8 nodes (proficient)
   - testing: 3 nodes (needs improvement) ⚠️
```

### 行动
```
发现 testing 知识薄弱，应该：
1. 学习更多测试相关知识
2. 实践 TDD
3. 记录测试模式和最佳实践
```

## 示例 4: 跨项目知识复用

### 场景
在新项目中使用之前项目的经验。

### 对话
```
User: recall 之前项目中的 CI/CD 配置

Assistant: 使用 MCP 工具 mem0-memory/recall_context
→ 返回：
   - GitHub Actions workflow
   - Docker multi-stage build
   - Kubernetes deployment

User: 帮我应用这些配置到新项目

Assistant: [复用之前的配置...]
```

## 示例 5: 技能自动生成

### 场景
重复执行某个任务多次后，自动生成技能。

### 时间线
```
Week 1: 手动配置 MongoDB
Week 2: 再次配置 MongoDB
Week 3: 第三次配置 MongoDB

→ 自动生成技能：mongodb-setup

Week 4: 使用自动生成的技能
User: 帮我配置 MongoDB

Assistant: 使用 skill: mongodb-setup
→ 自动执行完整的配置流程
```

## 示例 6: 会话总结

### 场景
长时间会话后自动生成总结。

### 命令行
```bash
# 运行完整学习流程
opencode-auto-learn run

# 生成会话总结
→ 保存到 Obsidian: Session Summaries/2026-06-16.md
```

### 生成的总结
```markdown
# Session Summary - 2026-06-16

## Key Decisions
- 使用 PostgreSQL 而不是 MySQL
- 采用微服务架构

## Learnings
- 理解了 CQRS 模式
- 学习到 Event Sourcing 的优势

## Blockers Resolved
- 解决了数据库连接池问题
- 修复了 Docker 网络配置

## Generated Skills
- mongodb-setup
- docker-network-config
```

## 最佳实践示例

### 实践 1: 定期回顾
```bash
# 添加到 crontab，每周回顾
0 9 * * 1 opencode-auto-learn status
```

### 实践 2: 项目启动时加载上下文
```bash
# 在项目目录执行
opencode-auto-learn semantic-search "$(basename $PWD)"
```

### 实践 3: 决策标记
```
在 OpenCode 中使用：
"[DECISION] 我们选择使用 Redis 作为缓存"

→ 自动分类为 decision 类型
```