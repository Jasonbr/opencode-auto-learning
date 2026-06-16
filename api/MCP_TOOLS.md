# MCP 工具 API 参考

## 概述

Mem0 MCP Server 提供以下工具供 OpenCode 调用。

## 工具列表

### 1. recall_context

召回相关记忆。

**参数：**
- `query` (string, required): 搜索查询
- `limit` (integer, optional): 最大结果数，默认 5
- `category` (string, optional): 按分类过滤

**示例：**
```json
{
  "tool": "recall_context",
  "params": {
    "query": "deployment configuration",
    "limit": 5,
    "category": "DevOps"
  }
}
```

**返回：**
```json
{
  "content": "## 📚 Relevant Context...",
  "memories_count": 3
}
```

### 2. save_memory

保存记忆。

**参数：**
- `content` (string, required): 记忆内容
- `category` (string, optional): 分类，默认 "auto"
- `tags` (array, optional): 标签列表

**示例：**
```json
{
  "tool": "save_memory",
  "params": {
    "content": "决定使用 Docker",
    "category": "decision",
    "tags": ["docker", "deployment"]
  }
}
```

### 3. semantic_search

语义搜索。

**参数：**
- `query` (string, required): 搜索查询
- `limit` (integer, optional): 最大结果数，默认 5

**示例：**
```json
{
  "tool": "semantic_search",
  "params": {
    "query": "performance optimization",
    "limit": 5
  }
}
```

**返回：**
```json
{
  "query": "performance optimization",
  "results_count": 5,
  "results": [
    {
      "memory_id": "...",
      "content": "...",
      "category": "technical",
      "similarity": 0.95
    }
  ]
}
```

### 4. find_related

查找相关记忆。

**参数：**
- `memory_id` (string, required): 记忆 ID

**示例：**
```json
{
  "tool": "find_related",
  "params": {
    "memory_id": "docker-setup-20260616"
  }
}
```

### 5. get_clusters

获取知识聚类。

**示例：**
```json
{
  "tool": "get_clusters",
  "params": {}
}
```

**返回：**
```json
{
  "clusters_count": 3,
  "clusters": [
    {"keyword": "deployment", "nodes": 8, "size": 8},
    {"keyword": "kubernetes", "nodes": 5, "size": 5}
  ]
}
```

### 6. get_categories

获取所有分类。

**示例：**
```json
{
  "tool": "get_categories",
  "params": {}
}
```

### 7. summarize_session

生成会话总结。

**参数：**
- `summary` (string, required): 总结内容

## 错误处理

所有工具返回标准 JSON-RPC 2.0 格式：

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": { ... }
}
```

错误响应：
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "error": {
    "code": -32601,
    "message": "Method not found"
  }
}
```

## 命令行工具

### opencode-auto-learn

**子命令：**

- `run` - 运行完整学习流程
- `status` - 查看系统状态
- `semantic-search <query>` - 语义搜索
- `build-graph` - 构建知识图谱
- `related <memory_id>` - 查找相关记忆
- `clean` - 清理自动生成的技能