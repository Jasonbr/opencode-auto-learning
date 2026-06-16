#!/usr/bin/env python3
"""
OpenCode 语义搜索模块
使用本地向量嵌入实现语义搜索
"""

import sqlite3
import hashlib
import json
from pathlib import Path
from typing import List, Dict, Tuple
import re

class SemanticSearch:
    """语义搜索引擎"""
    
    def __init__(self):
        self.db_path = Path.home() / ".mem0" / "vector_memory.db"
        self.memory_dir = Path.home() / ".config/opencode/memory/user"
        self._init_db()
    
    def _init_db(self):
        """初始化向量数据库"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS vectors (
                id INTEGER PRIMARY KEY,
                memory_id TEXT UNIQUE,
                content TEXT,
                embedding BLOB,
                category TEXT,
                metadata TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_category ON vectors(category)
        """)
        
        conn.commit()
        conn.close()
    
    def _simple_embedding(self, text: str) -> bytes:
        """
        简化的嵌入生成（使用词袋模型 + TF-IDF 思想）
        实际生产环境应使用 sentence-transformers 或 OpenAI API
        """
        # 预处理
        text = text.lower()
        text = re.sub(r'[^\\w\\s]', ' ', text)
        words = text.split()
        
        # 构建词频向量（简化版）
        word_freq = {}
        for word in words:
            if len(word) > 2:  # 过滤短词
                word_freq[word] = word_freq.get(word, 0) + 1
        
        # 使用哈希作为简化嵌入
        embedding = []
        for i in range(128):  # 128维向量
            hash_val = hashlib.md5(f"{i}:{json.dumps(word_freq, sort_keys=True)}".encode()).hexdigest()
            val = int(hash_val[:8], 16) % 1000 / 1000.0
            embedding.append(val)
        
        return json.dumps(embedding).encode()
    
    def _cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """计算余弦相似度"""
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        norm1 = sum(a * a for a in vec1) ** 0.5
        norm2 = sum(b * b for b in vec2) ** 0.5
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return dot_product / (norm1 * norm2)
    
    def index_memory(self, memory_id: str, content: str, category: str = "general", metadata: Dict = None):
        """索引记忆"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        embedding = self._simple_embedding(content)
        
        cursor.execute("""
            INSERT OR REPLACE INTO vectors (memory_id, content, embedding, category, metadata)
            VALUES (?, ?, ?, ?, ?)
        """, (memory_id, content, embedding, category, json.dumps(metadata or {})))
        
        conn.commit()
        conn.close()
    
    def search(self, query: str, category: str = None, top_k: int = 5) -> List[Dict]:
        """语义搜索"""
        query_embedding = json.loads(self._simple_embedding(query))
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if category:
            cursor.execute("""
                SELECT memory_id, content, embedding, category, metadata
                FROM vectors
                WHERE category = ?
            """, (category,))
        else:
            cursor.execute("""
                SELECT memory_id, content, embedding, category, metadata
                FROM vectors
            """)
        
        results = []
        for row in cursor.fetchall():
            memory_id, content, embedding_blob, cat, metadata_str = row
            
            memory_embedding = json.loads(embedding_blob)
            similarity = self._cosine_similarity(query_embedding, memory_embedding)
            
            results.append({
                "memory_id": memory_id,
                "content": content,
                "category": cat,
                "metadata": json.loads(metadata_str),
                "similarity": similarity
            })
        
        conn.close()
        
        # 按相似度排序
        results.sort(key=lambda x: x["similarity"], reverse=True)
        
        return results[:top_k]
    
    def build_index(self):
        """从记忆文件构建索引"""
        count = 0
        
        for memory_file in self.memory_dir.glob("*.md"):
            content = memory_file.read_text()
            
            # 解析 frontmatter
            if content.startswith("---"):
                parts = content.split("---", 2)
                if len(parts) >= 3:
                    try:
                        metadata = json.loads(parts[1]) if parts[1].strip().startswith("{") else {}
                    except:
                        metadata = {}
                    content_text = parts[2].strip()
                else:
                    metadata = {}
                    content_text = content
            else:
                metadata = {}
                content_text = content
            
            # 索引
            self.index_memory(
                memory_id=memory_file.stem,
                content=content_text[:1000],  # 限制长度
                category=metadata.get("type", "general"),
                metadata=metadata
            )
            count += 1
        
        return count
    
    def find_similar(self, memory_id: str, top_k: int = 5) -> List[Dict]:
        """查找相似记忆"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT embedding FROM vectors WHERE memory_id = ?", (memory_id,))
        result = cursor.fetchone()
        
        if not result:
            conn.close()
            return []
        
        target_embedding = json.loads(result[0])
        
        # 查找相似
        cursor.execute("SELECT memory_id, content, embedding, category FROM vectors WHERE memory_id != ?", (memory_id,))
        
        results = []
        for row in cursor.fetchall():
            mid, content, embedding_blob, cat = row
            memory_embedding = json.loads(embedding_blob)
            similarity = self._cosine_similarity(target_embedding, memory_embedding)
            
            if similarity > 0.5:  # 相似度阈值
                results.append({
                    "memory_id": mid,
                    "content": content[:200],
                    "category": cat,
                    "similarity": similarity
                })
        
        conn.close()
        
        results.sort(key=lambda x: x["similarity"], reverse=True)
        return results[:top_k]

if __name__ == "__main__":
    import sys
    
    search = SemanticSearch()
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "build":
            count = search.build_index()
            print(f"✅ Indexed {count} memories")
        elif sys.argv[1] == "search" and len(sys.argv) > 2:
            query = sys.argv[2]
            results = search.search(query, top_k=5)
            print(f"🔍 Search results for: {query}")
            for r in results:
                print(f"  [{r['similarity']:.2%}] {r['category']}: {r['content'][:80]}...")
        elif sys.argv[1] == "similar" and len(sys.argv) > 2:
            memory_id = sys.argv[2]
            results = search.find_similar(memory_id)
            print(f"🔍 Memories similar to: {memory_id}")
            for r in results:
                print(f"  [{r['similarity']:.2%}] {r['category']}: {r['content'][:80]}...")
        else:
            print("Usage: semantic_search.py [build|search <query>|similar <memory_id>]")
    else:
        # 默认构建索引
        count = search.build_index()
        print(f"✅ Indexed {count} memories")
