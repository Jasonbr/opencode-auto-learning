#!/usr/bin/env python3
"""
增强版记忆管理系统
- 语义搜索
- 会话状态保持
- 自动分类
- Obsidian 深度集成
"""

import json
import sqlite3
import hashlib
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional

class EnhancedMemoryStore:
    """增强版记忆存储"""
    
    def __init__(self, db_path: str = "~/.mem0/enhanced_memory.db"):
        self.db_path = Path(db_path).expanduser()
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
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
                importance INTEGER DEFAULT 5,
                access_count INTEGER DEFAULT 0,
                last_accessed TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # 会话表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                session_id TEXT UNIQUE,
                title TEXT,
                summary TEXT,
                messages TEXT,
                file_context TEXT,
                cursor_position TEXT,
                metadata TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # 索引
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_memories_user ON memories(user_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_memories_category ON memories(category)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_memories_importance ON memories(importance)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_sessions_user ON sessions(user_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_sessions_session ON sessions(session_id)")
        
        conn.commit()
        conn.close()
    
    def add(self, content: str, user_id: str, metadata: Dict = None) -> Dict:
        """添加记忆"""
        # 生成简单嵌入
        embedding = self._simple_embed(content)
        
        # 自动分类
        category = self._auto_categorize(content)
        if metadata and metadata.get('category') and metadata['category'] != 'auto':
            category = metadata['category']
        
        # 计算重要性
        importance = self._calculate_importance(content)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO memories 
            (user_id, content, embedding, category, tags, metadata, importance, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            user_id, content, json.dumps(embedding), category,
            json.dumps(metadata.get('tags', [])) if metadata else '[]',
            json.dumps(metadata) if metadata else '{}',
            importance,
            datetime.now().isoformat()
        ))
        
        memory_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return {"id": memory_id, "category": category, "importance": importance}
    
    def search(self, query: str, user_id: str, limit: int = 5,
               category: str = None, min_importance: int = 1) -> List[Dict]:
        """语义搜索记忆"""
        query_embedding = self._simple_embed(query)
        query_words = set(query.lower().split())
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if category:
            cursor.execute("""
                SELECT * FROM memories 
                WHERE user_id = ? AND category = ? AND importance >= ?
                ORDER BY last_accessed DESC NULLS LAST, created_at DESC
                LIMIT ?
            """, (user_id, category, min_importance, limit * 2))
        else:
            cursor.execute("""
                SELECT * FROM memories 
                WHERE user_id = ? AND importance >= ?
                ORDER BY last_accessed DESC NULLS LAST, created_at DESC
                LIMIT ?
            """, (user_id, min_importance, limit * 2))
        
        results = cursor.fetchall()
        conn.close()
        
        # 计算相关性分数
        scored_results = []
        for row in results:
            content = row[2]
            content_words = set(content.lower().split())
            
            # 简单的词袋模型相关性
            relevance = len(query_words & content_words)
            
            # 提升精确匹配
            if query.lower() in content.lower():
                relevance += 10
            
            # 根据重要性加权
            importance = row[7]
            relevance += importance * 0.5
            
            scored_results.append((relevance, row))
        
        # 排序并返回
        scored_results.sort(key=lambda x: x[0], reverse=True)
        
        memories = []
        for relevance, row in scored_results[:limit]:
            memories.append({
                "id": row[0],
                "content": row[2],
                "category": row[4],
                "tags": json.loads(row[5]),
                "metadata": json.loads(row[6]),
                "importance": row[7],
                "created_at": row[9],
                "relevance": relevance
            })
        
        return memories
    
    def get_recent_context(self, user_id: str, hours: int = 24) -> List[Dict]:
        """获取最近上下文"""
        since = (datetime.now() - timedelta(hours=hours)).isoformat()
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM memories 
            WHERE user_id = ? AND created_at > ?
            ORDER BY created_at DESC
        """, (user_id, since))
        
        results = cursor.fetchall()
        conn.close()
        
        return [
            {
                "id": row[0],
                "content": row[2],
                "category": row[4],
                "created_at": row[9]
            }
            for row in results
        ]
    
    def save_session(self, session_data: Dict) -> Dict:
        """保存完整会话"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        session_id = session_data.get('session_id', f"sess_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        
        cursor.execute("""
            INSERT OR REPLACE INTO sessions
            (user_id, session_id, title, summary, messages, file_context, cursor_position, metadata, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            session_data.get('user_id', 'xiaoxi'),
            session_id,
            session_data.get('title', 'Untitled'),
            session_data.get('summary', ''),
            json.dumps(session_data.get('messages', [])),
            json.dumps(session_data.get('file_context', {})),
            json.dumps(session_data.get('cursor_position', {})),
            json.dumps(session_data.get('metadata', {})),
            datetime.now().isoformat()
        ))
        
        conn.commit()
        conn.close()
        
        return {"session_id": session_id, "status": "saved"}
    
    def load_session(self, session_id: str) -> Optional[Dict]:
        """加载会话"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM sessions WHERE session_id = ?
        """, (session_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if not row:
            return None
        
        return {
            "session_id": row[2],
            "title": row[3],
            "summary": row[4],
            "messages": json.loads(row[5]),
            "file_context": json.loads(row[6]),
            "cursor_position": json.loads(row[7]),
            "metadata": json.loads(row[8]),
            "created_at": row[9],
            "updated_at": row[10]
        }
    
    def get_all_sessions(self, user_id: str) -> List[Dict]:
        """获取所有会话"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT session_id, title, summary, updated_at 
            FROM sessions 
            WHERE user_id = ?
            ORDER BY updated_at DESC
        """, (user_id,))
        
        results = cursor.fetchall()
        conn.close()
        
        return [
            {
                "session_id": row[0],
                "title": row[1],
                "summary": row[2],
                "updated_at": row[3]
            }
            for row in results
        ]
    
    def _simple_embed(self, text: str, dim: int = 128) -> List[float]:
        """生成简单嵌入向量"""
        # 使用字符级哈希生成确定性嵌入
        embedding = []
        for i in range(dim):
            char = text[i % len(text)] if i < len(text) else text[-1]
            hash_val = hash((i, ord(char), len(text))) % 10000 / 10000
            embedding.append(hash_val)
        return embedding
    
    def _auto_categorize(self, content: str) -> str:
        """自动分类"""
        content_lower = content.lower()
        
        categories = {
            "AI": ["model", "training", "llm", "embedding", "ai", "ml", "模型", "训练"],
            "DevOps": ["deploy", "docker", "k8s", "server", "部署", "运维", "监控"],
            "Programming": ["code", "function", "class", "api", "代码", "函数", "编程"],
            "Project": ["requirement", "feature", "需求", "功能", "项目"],
            "Memory": ["memory", "recall", "remember", "记忆", "回忆"],
            "OpenCode": ["opencode", "mcp", "cursor", "claude", "编辑器"]
        }
        
        scores = {cat: 0 for cat in categories}
        for cat, keywords in categories.items():
            for kw in keywords:
                if kw in content_lower:
                    scores[cat] += 1
        
        if max(scores.values()) > 0:
            return max(scores, key=scores.get)
        
        return "general"
    
    def _calculate_importance(self, content: str) -> int:
        """计算内容重要性"""
        importance = 5  # 基础分
        
        # 关键词加权
        high_importance = ["decision", "conclusion", "fix", "bug", "error", 
                          "结论", "决定", "修复", "错误", "解决"]
        for word in high_importance:
            if word in content.lower():
                importance += 2
        
        # 长度加权（适中长度更重要）
        length = len(content)
        if 100 < length < 1000:
            importance += 1
        
        return min(importance, 10)  # 最高10分

# 导出类
if __name__ == "__main__":
    store = EnhancedMemoryStore()
    print("✅ Enhanced memory store initialized")
