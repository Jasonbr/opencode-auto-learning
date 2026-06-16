#!/usr/bin/env python3
"""
Mem0 MCP Server for OpenCode - Qwen 3.7 Plus Edition
适配 OpenCode 的 Bailian provider，使用本地向量数据库
"""

import json
import sys
import os
import asyncio
import sqlite3
import hashlib
from typing import Any, Dict, List, Optional
from datetime import datetime, timedelta
from pathlib import Path
import re

# 导入增强版记忆存储
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from enhanced_memory import EnhancedMemoryStore

class SimpleEmbedder:
    """简化版嵌入生成器（不使用外部 API）"""
    
    def __init__(self, dim: int = 1536):
        self.dim = dim
    
    def embed(self, text: str) -> List[float]:
        """生成简单的哈希嵌入（用于演示，实际可用 sentence-transformers）"""
        # 使用哈希生成确定性嵌入
        hash_val = hashlib.sha256(text.encode()).hexdigest()
        embedding = []
        for i in range(0, min(len(hash_val), self.dim * 2), 2):
            val = int(hash_val[i:i+2], 16) / 255.0
            embedding.append(val)
        
        # 填充到指定维度
        while len(embedding) < self.dim:
            embedding.extend(embedding[:self.dim - len(embedding)])
        
        return embedding[:self.dim]

class SimpleMemoryStore:
    """基于 SQLite 的简化记忆存储"""
    
    def __init__(self, db_path: str = "~/.mem0/local_memory.db"):
        self.db_path = os.path.expanduser(db_path)
        self.embedder = SimpleEmbedder()
        self._init_db()
    
    def _init_db(self):
        """初始化数据库"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 记忆表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                content TEXT NOT NULL,
                embedding BLOB,
                category TEXT DEFAULT 'general',
                tags TEXT,
                metadata TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # 创建索引
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_user ON memories(user_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_category ON memories(category)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_created ON memories(created_at)")
        
        conn.commit()
        conn.close()
    
    def add(self, content: str, user_id: str, metadata: Dict = None) -> Dict:
        """添加记忆"""
        embedding = self.embedder.embed(content)
        embedding_blob = json.dumps(embedding).encode()
        
        category = metadata.get('category', 'general') if metadata else 'general'
        tags = json.dumps(metadata.get('tags', [])) if metadata else '[]'
        meta_json = json.dumps(metadata) if metadata else '{}'
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO memories (user_id, content, embedding, category, tags, metadata)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (user_id, content, embedding_blob, category, tags, meta_json))
        
        memory_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return {"id": memory_id, "status": "saved"}
    
    def search(self, query: str, user_id: str, limit: int = 5, 
               category: str = None) -> List[Dict]:
        """搜索记忆（简化版：关键词匹配 + 时间排序）"""
        query_embedding = self.embedder.embed(query)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if category:
            cursor.execute("""
                SELECT id, content, category, tags, metadata, created_at
                FROM memories
                WHERE user_id = ? AND category = ?
                ORDER BY created_at DESC
                LIMIT ?
            """, (user_id, category, limit * 10))
        else:
            cursor.execute("""
                SELECT id, content, category, tags, metadata, created_at
                FROM memories
                WHERE user_id = ?
                ORDER BY created_at DESC
                LIMIT ?
            """, (user_id, limit * 10))
        
        results = cursor.fetchall()
        conn.close()
        
        # 简单的相关性排序（关键词匹配）
        query_words = set(query.lower().split())
        scored_results = []
        
        for row in results:
            content = row[1]
            content_words = set(content.lower().split())
            score = len(query_words & content_words)
            scored_results.append((score, row))
        
        # 按分数排序
        scored_results.sort(key=lambda x: x[0], reverse=True)
        
        # 格式化结果
        memories = []
        for score, row in scored_results[:limit]:
            memories.append({
                "id": row[0],
                "memory": row[1],
                "category": row[2],
                "tags": json.loads(row[3]),
                "metadata": json.loads(row[4]),
                "created_at": row[5],
                "relevance_score": score
            })
        
        return memories
    
    def get_recent(self, user_id: str, limit: int = 10) -> List[Dict]:
        """获取最近的记忆"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, content, category, tags, metadata, created_at
            FROM memories
            WHERE user_id = ?
            ORDER BY created_at DESC
            LIMIT ?
        """, (user_id, limit))
        
        results = cursor.fetchall()
        conn.close()
        
        return [
            {
                "id": row[0],
                "memory": row[1],
                "category": row[2],
                "tags": json.loads(row[3]),
                "metadata": json.loads(row[4]),
                "created_at": row[5]
            }
            for row in results
        ]
    
    def get_categories(self, user_id: str) -> List[str]:
        """获取所有分类"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT DISTINCT category FROM memories WHERE user_id = ?
        """, (user_id,))
        
        results = cursor.fetchall()
        conn.close()
        
        return [row[0] for row in results]

class Mem0MCPServer:
    def __init__(self):
        self.user_id = "xiaoxi"
        self.memory = SimpleMemoryStore()
        self.obsidian_vault = Path.home() / "Documents/Obsidian Vault"
        self.knowledge_dir = self.obsidian_vault / "Knowledge"
        
        print(f"[Mem0 MCP] Server initialized", file=sys.stderr)
        print(f"[Mem0 MCP] Memory DB: ~/.mem0/local_memory.db", file=sys.stderr)
        
    async def handle_request(self, request: Dict) -> Dict:
        """处理 MCP 请求"""
        method = request.get("method", "")
        params = request.get("params", {})
        request_id = request.get("id", 1)
        
        print(f"[Mem0 MCP] Method: {method}", file=sys.stderr)
        
        try:
            # 处理 MCP 协议方法
            if method == "initialize":
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "capabilities": {
                            "tools": {}
                        },
                        "serverInfo": {
                            "name": "mem0-memory",
                            "version": "1.0.0"
                        }
                    }
                }
            elif method == "tools/list":
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "tools": [
                            {
                                "name": "recall_context",
                                "description": "Recall relevant memories and context for the current task",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "query": {"type": "string", "description": "Search query for memories"},
                                        "limit": {"type": "integer", "description": "Max number of results", "default": 5},
                                        "category": {"type": "string", "description": "Filter by category"}
                                    },
                                    "required": ["query"]
                                }
                            },
                            {
                                "name": "save_memory",
                                "description": "Save important information to memory",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "content": {"type": "string", "description": "Content to save"},
                                        "category": {"type": "string", "description": "Category (auto, technical, decision, etc.)", "default": "auto"},
                                        "tags": {"type": "array", "items": {"type": "string"}, "description": "Tags for the memory"}
                                    },
                                    "required": ["content"]
                                }
                            },
                            {
                                "name": "search_knowledge",
                                "description": "Search Obsidian knowledge vault",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "query": {"type": "string", "description": "Search query"},
                                        "limit": {"type": "integer", "description": "Max results", "default": 5}
                                    },
                                    "required": ["query"]
                                }
                            },
                            {
                                "name": "summarize_session",
                                "description": "Summarize current session and save to Obsidian",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "summary": {"type": "string", "description": "Session summary"}
                                    },
                                    "required": ["summary"]
                                }
                            },
                            {
                                "name": "get_categories",
                                "description": "Get all memory categories",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {}
                                }
                            },
                            {
                                "name": "get_recent",
                                "description": "Get recent memories",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "limit": {"type": "integer", "description": "Max results", "default": 10}
                                    }
                                }
                            }
                        ]
                    }
                }
            elif method == "tools/call":
                tool = params.get("name", "")
                arguments = params.get("arguments", {})
                return await self.call_tool(tool, arguments, request_id)
            elif method.startswith("notifications/"):
                return None
            else:
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "error": {"code": -32601, "message": f"Method not found: {method}"}
                }
        except Exception as e:
            import traceback
            traceback.print_exc(file=sys.stderr)
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {"code": -32603, "message": f"Internal error: {str(e)}"}
            }
    
    async def call_tool(self, tool: str, params: Dict, request_id: int) -> Dict:
        try:
            if tool == "recall_context":
                result = await self.recall_context(params)
            elif tool == "save_memory":
                result = await self.save_memory(params)
            elif tool == "search_knowledge":
                result = await self.search_knowledge(params)
            elif tool == "summarize_session":
                result = await self.summarize_session(params)
            elif tool == "get_categories":
                result = await self.get_categories(params)
            elif tool == "get_recent":
                result = await self.get_recent(params)
            elif tool == "semantic_search":
                result = await self.semantic_search(params)
            elif tool == "find_related":
                result = await self.find_related(params)
            elif tool == "get_clusters":
                result = await self.get_clusters(params)
            else:
                result = {"error": f"Unknown tool: {tool}"}
            
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "content": [{"type": "text", "text": json.dumps(result, ensure_ascii=False, indent=2)}]
                }
            }
        except Exception as e:
            import traceback
            traceback.print_exc(file=sys.stderr)
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {"code": -32603, "message": f"Tool execution failed: {str(e)}"}
            }
    
    async def recall_context(self, params: Dict) -> Dict:
        """Recall 相关记忆"""
        query = params.get("query", "")
        limit = params.get("limit", 5)
        category = params.get("category")
        
        if not query:
            return {"content": "No query provided", "memories_count": 0}
        
        memories = self.memory.search(
            query=query,
            user_id=self.user_id,
            limit=limit,
            category=category
        )
        
        context = self._format_memories(memories, query)
        
        return {
            "content": context,
            "memories_count": len(memories),
            "query": query
        }
    
    async def save_memory(self, params: Dict) -> Dict:
        """保存重要记忆"""
        content = params.get("content", "")
        category = params.get("category", "auto")
        tags = params.get("tags", [])
        
        if not content:
            return {"error": "No content to save"}
        
        # 自动分类
        if category == "auto":
            category = self._auto_categorize(content)
        
        result = self.memory.add(
            content=content,
            user_id=self.user_id,
            metadata={
                "category": category,
                "tags": tags,
                "source": "opencode",
                "timestamp": datetime.now().isoformat()
            }
        )
        
        # 同步到 Obsidian
        await self._sync_to_obsidian(content, category, tags)
        
        return {
            "status": "saved",
            "category": category,
            "memory_id": result.get("id")
        }
    
    async def search_knowledge(self, params: Dict) -> Dict:
        """搜索 Obsidian 知识库"""
        query = params.get("query", "")
        limit = params.get("limit", 5)
        
        if not self.obsidian_vault.exists():
            return {
                "error": "Obsidian vault not found",
                "results": []
            }
        
        results = []
        query_lower = query.lower()
        
        for md_file in self.obsidian_vault.rglob("*.md"):
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if query_lower in content.lower():
                        lines = content.split('\n')
                        for i, line in enumerate(lines):
                            if query_lower in line.lower():
                                start = max(0, i - 2)
                                end = min(len(lines), i + 3)
                                snippet = '\n'.join(lines[start:end])
                                results.append({
                                    "file": str(md_file).replace(str(self.obsidian_vault) + "/", ""),
                                    "line": i + 1,
                                    "snippet": snippet[:500]
                                })
                                break
            except Exception:
                continue
            
            if len(results) >= limit:
                break
        
        return {"results": results, "query": query, "found": len(results)}
        
        contents = []
        for f in files:
            if f and os.path.exists(f):
                try:
                    with open(f, 'r', encoding='utf-8') as file:
                        content = file.read()
                        contents.append({
                            "file": Path(f).name,
                            "path": f,
                            "preview": content[:500] + "..." if len(content) > 500 else content
                        })
                except:
                    pass
        
        return {
            "results": contents,
            "query": query,
            "found": len(contents)
        }
    
    async def summarize_session(self, params: Dict) -> Dict:
        """总结当前会话（简化版，实际总结由 OpenCode 的 Qwen 完成）"""
        session_content = params.get("content", "")
        
        if not session_content:
            return {"error": "No session content"}
        
        # 提取关键行
        lines = session_content.split("\n")
        important_lines = []
        keywords = [
            "decision", "conclusion", "fix", "implement", "add", "create",
            "update", "delete", "完成", "结论", "决定", "修复", "实现",
            "添加", "创建", "更新", "删除", "解决", "问题", "方案"
        ]
        
        for line in lines:
            if any(kw in line.lower() for kw in keywords):
                important_lines.append(line.strip())
        
        summary = "\n".join(important_lines[:10]) if important_lines else "Session discussion"
        
        # 保存到记忆
        self.memory.add(
            content=f"Session Summary: {summary}",
            user_id=self.user_id,
            metadata={
                "type": "session_summary",
                "source": "opencode",
                "timestamp": datetime.now().isoformat()
            }
        )
        
        # 同步到 Obsidian
        await self._save_to_obsidian(summary)
        
        return {"summary": summary}
    
    async def get_categories(self, params: Dict) -> Dict:
        """获取所有分类"""
        categories = self.memory.get_categories(self.user_id)
        if not categories:
            categories = ["general"]
        return {"categories": categories}
    
    async def semantic_search(self, params: Dict) -> Dict:
        """语义搜索"""
        from semantic_search import SemanticSearch
        
        query = params.get("query", "")
        top_k = params.get("limit", 5)
        
        if not query:
            return {"error": "No query provided"}
        
        search = SemanticSearch()
        results = search.search(query, top_k=top_k)
        
        return {
            "query": query,
            "results_count": len(results),
            "results": results
        }
    
    async def find_related(self, params: Dict) -> Dict:
        """查找相关记忆"""
        from knowledge_graph import KnowledgeGraph
        
        memory_id = params.get("memory_id", "")
        
        if not memory_id:
            return {"error": "No memory_id provided"}
        
        kg = KnowledgeGraph()
        related = kg.get_related(memory_id)
        
        return {
            "memory_id": memory_id,
            "direct_count": len(related["direct"]),
            "related": related
        }
    
    async def get_clusters(self, params: Dict) -> Dict:
        """获取知识聚类"""
        from knowledge_graph import KnowledgeGraph
        
        kg = KnowledgeGraph()
        clusters = kg.find_clusters()
        
        return {
            "clusters_count": len(clusters),
            "clusters": clusters
        }
    
    def _format_memories(self, memories: List, query: str = "") -> str:
        """格式化记忆为文本"""
        if not memories:
            return "**No relevant memories found.**"
        
        formatted = [f"## 📚 Relevant Context for: _{query}_\n"]
        
        for i, mem in enumerate(memories, 1):
            memory_text = mem.get("memory", "")
            category = mem.get("category", "general")
            relevance = mem.get("relevance_score", 0)
            
            formatted.append(f"{i}. **[{category.upper()}]** {memory_text}")
            if relevance > 0:
                formatted.append(f"   _Relevance: {relevance}_")
            formatted.append("")
        
        return "\n".join(formatted)
    
    def _auto_categorize(self, content: str) -> str:
        """自动分类记忆"""
        content_lower = content.lower()
        
        categories = {
            "AI": ["model", "training", "inference", "prompt", "llm", "embedding", "vector", "ai", "ml", "模型", "训练", "推理", "嵌入"],
            "DevOps": ["deploy", "docker", "k8s", "kubernetes", "server", "infra", "monitoring", "deployment", "部署", "运维", "监控", "服务器"],
            "Programming": ["code", "bug", "fix", "refactor", "function", "class", "api", "library", "代码", "函数", "类", "修复", "bug", "编程"],
            "Project": ["requirement", "feature", "迭代", "version", "milestone", "需求", "功能", "版本", "里程碑", "项目"],
            "OpenCode": ["opencode", "mcp", "ide", "editor", "cursor", "claude", "插件"],
            "Memory": ["memory", "mem0", "remember", "recall", "记忆", "回忆", "存储"]
        }
        
        scores = {cat: 0 for cat in categories}
        
        for cat, keywords in categories.items():
            for keyword in keywords:
                if keyword in content_lower:
                    scores[cat] += 1
        
        if max(scores.values()) > 0:
            return max(scores, key=scores.get)
        
        return "general"
    
    async def _sync_to_obsidian(self, content: str, category: str, tags: List):
        """同步到 Obsidian"""
        if not self.obsidian_vault.exists():
            return
        
        mem0_dir = self.obsidian_vault / "opencode-memory" / "mem0"
        mem0_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        slug = content[:30].replace(" ", "-").replace("/", "-")
        filename = f"{timestamp}-{slug}.md"
        
        note_path = mem0_dir / filename
        with open(note_path, 'w', encoding='utf-8') as f:
            f.write(f"---\n")
            f.write(f"category: {category}\n")
            f.write(f"tags: [{', '.join(tags)}]\n")
            f.write(f"source: mem0-mcp\n")
            f.write(f"created: {datetime.now().isoformat()}\n")
            f.write(f"---\n\n")
            f.write(f"# {category}\n\n")
            f.write(f"{content}\n")
    
    async def _save_to_obsidian(self, summary: str):
        """保存到 Obsidian"""
        if not self.obsidian_vault.exists():
            return
        
        today = datetime.now().strftime("%Y-%m-%d")
        session_dir = self.obsidian_vault / "Session Summaries"
        session_dir.mkdir(exist_ok=True)
        
        note_path = session_dir / f"{today}.md"
        
        with open(note_path, 'a', encoding='utf-8') as f:
            f.write(f"\n\n## {datetime.now().strftime('%H:%M:%S')}\n")
            f.write(summary)
            f.write("\n\n---\n")

async def main():
    server = Mem0MCPServer()
    
    print("[Mem0 MCP] Server started, waiting for requests...", file=sys.stderr)
    
    while True:
        try:
            line = input()
            if not line:
                continue
            
            request = json.loads(line)
            response = await server.handle_request(request)
            
            if response is not None:
                print(json.dumps(response), flush=True)
            
        except EOFError:
            print("[Mem0 MCP] EOF received, shutting down", file=sys.stderr)
            break
        except json.JSONDecodeError as e:
            print(json.dumps({"error": f"Invalid JSON: {str(e)}"}), flush=True)
        except Exception as e:
            import traceback
            traceback.print_exc(file=sys.stderr)
            print(json.dumps({"error": f"Server error: {str(e)}"}), flush=True)

if __name__ == "__main__":
    asyncio.run(main())
