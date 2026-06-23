# Changelog

所有显著的变更都将记录在此文件中。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)。

## [1.0.0] - 2026-06-23

### ✨ 新增

- 🧠 **记忆提取系统 V2** - 智能从会话提取 5 类记忆
  - decision: 技术决策
  - learning: 学习笔记  
  - error-solution: 错误解决方案
  - config: 配置模式
  - command: 常用命令
  
- 🔨 **技能生成器 V3** - 基于记忆自动生成 Skill
  - 修复 frontmatter 解析
  - 支持 5 种记忆类型
  - 自动内容清洗
  
- 🔌 **MCP Server** - Mem0 记忆层 MCP 集成
  - JSON-RPC 2.0 协议
  - semantic_search 工具
  - recall_context / save_memory
  
- 🔄 **Hermes 桥接** - 双向同步记忆
  - 导出到 Hermes
  - 归档到 Obsidian
  - 自动分类
  
- 📜 **AI 编码规则** - 4 个核心规则
  - TDD 强制规则
  - Three-Strikes 规则
  - 预提交验证
  - 执行纪律
  
- ⚡ **自动运行** - LaunchAgent 定时任务
  - 每日凌晨 3:00 自动运行
  - 状态报告
  - 错误日志

### 📊 数据

- 提取记忆: 1,297 条
- 会话文件: 42 个
- 生成技能: 5 个分类

### 🔧 技术细节

- Python 3.10+
- SQLite 向量存储
- 余弦相似度搜索
- 关键词共现聚类

### ⚠️ 已知限制

- OpenCode 1.15.7 不支持顶层 "rules" 键
- 规则需通过 oh-my-openagent 或其他方式加载
- 向量嵌入使用简化哈希算法（非 sentence-transformers）

### 📝 依赖

- Python 3.10+
- sqlite3 (内建)
- asyncio
- pathlib

---

## [0.9.0] - 2026-06-18

### 预览版

- 基础记忆提取
- 简单技能生成
- MCP Server 原型

---

## 计划

### [1.1.0] - 计划中

- [ ] 语义搜索增强 (sentence-transformers)
- [ ] 知识图谱可视化
- [ ] 主动推荐系统
- [ ] Web UI 管理界面
- [ ] 多模态记忆支持

### [2.0.0] - 远景

- [ ] 跨平台支持 (Linux/Windows)
- [ ] 分布式记忆存储
- [ ] 机器学习模式识别
- [ ] 自动架构建议
