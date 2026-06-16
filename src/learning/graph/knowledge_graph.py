#!/usr/bin/env python3
"""
OpenCode 知识图谱模块
构建记忆之间的关联网络
"""

import json
import sqlite3
from pathlib import Path
from typing import List, Dict, Set, Tuple
from collections import defaultdict
import re

class KnowledgeGraph:
    """知识图谱"""
    
    def __init__(self):
        self.db_path = Path.home() / ".mem0" / "knowledge_graph.db"
        self.memory_dir = Path.home() / ".config/opencode/memory/user"
        self._init_db()
    
    def _init_db(self):
        """初始化图数据库"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 节点表（记忆）
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS nodes (
                id TEXT PRIMARY KEY,
                content TEXT,
                category TEXT,
                metadata TEXT,
                weight REAL DEFAULT 1.0
            )
        """)
        
        # 边表（关联）
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS edges (
                source TEXT,
                target TEXT,
                relation TEXT,
                weight REAL DEFAULT 1.0,
                PRIMARY KEY (source, target, relation),
                FOREIGN KEY (source) REFERENCES nodes(id),
                FOREIGN KEY (target) REFERENCES nodes(id)
            )
        """)
        
        # 关键词表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS keywords (
                node_id TEXT,
                keyword TEXT,
                frequency INTEGER,
                PRIMARY KEY (node_id, keyword),
                FOREIGN KEY (node_id) REFERENCES nodes(id)
            )
        """)
        
        conn.commit()
        conn.close()
    
    def _extract_keywords(self, text: str) -> List[str]:
        """提取关键词"""
        # 简单关键词提取（停用词过滤）
        stop_words = {'the', 'a', 'an', 'in', 'on', 'at', 'to', 'for', 'of', 'is', 'are', 
                      '的', '了', '在', '是', '和', '与', '对', '为', '有', '我', '你', '他'}
        
        text = re.sub(r'[^\w\s]', ' ', text.lower())
        words = [w for w in text.split() if len(w) > 2 and w not in stop_words]
        
        # 返回高频词
        word_freq = defaultdict(int)
        for word in words:
            word_freq[word] += 1
        
        return [w for w, c in sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:10]]
    
    def _find_relations(self, node1: Dict, node2: Dict) -> List[str]:
        """发现两个节点之间的关系"""
        relations = []
        
        # 1. 相同分类
        if node1.get('category') == node2.get('category'):
            relations.append('same_category')
        
        # 2. 关键词重叠
        keywords1 = set(self._extract_keywords(node1.get('content', '')))
        keywords2 = set(self._extract_keywords(node2.get('content', '')))
        
        overlap = keywords1 & keywords2
        if len(overlap) >= 2:
            relations.append('keyword_overlap')
        
        return relations
    
    def build_graph(self):
        """构建知识图谱"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 清空现有数据
        cursor.execute("DELETE FROM edges")
        cursor.execute("DELETE FROM keywords")
        cursor.execute("DELETE FROM nodes")
        
        # 加载所有记忆
        memories = []
        for memory_file in self.memory_dir.glob("*.md"):
            content = memory_file.read_text()
            
            memories.append({
                "id": memory_file.stem,
                "content": content,
                "category": "general"
            })
            
            cursor.execute("""
                INSERT OR REPLACE INTO nodes (id, content, category, metadata)
                VALUES (?, ?, ?, ?)
            """, (memory_file.stem, content[:500], "general", "{}"))
            
            # 插入关键词
            keywords = self._extract_keywords(content)
            for keyword in keywords:
                cursor.execute("""
                    INSERT OR REPLACE INTO keywords (node_id, keyword, frequency)
                    VALUES (?, ?, ?)
                """, (memory_file.stem, keyword, 1))
        
        conn.commit()
        
        # 建立边
        edge_count = 0
        for i, node1 in enumerate(memories):
            for node2 in memories[i+1:]:
                relations = self._find_relations(node1, node2)
                for relation in relations:
                    cursor.execute("""
                        INSERT OR REPLACE INTO edges (source, target, relation, weight)
                        VALUES (?, ?, ?, ?)
                    """, (node1["id"], node2["id"], relation, 0.5))
                    edge_count += 1
        
        conn.commit()
        conn.close()
        
        return len(memories), edge_count
    
    def get_related(self, memory_id: str, depth: int = 1) -> Dict:
        """获取相关记忆"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT target, relation, weight FROM edges WHERE source = ?
            UNION
            SELECT source, relation, weight FROM edges WHERE target = ?
        """, (memory_id, memory_id))
        
        direct = cursor.fetchall()
        conn.close()
        
        return {
            "direct": [{"id": r[0], "relation": r[1], "weight": r[2]} for r in direct]
        }
    
    def find_clusters(self) -> List[Dict]:
        """发现知识聚类"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT keyword, GROUP_CONCAT(node_id) as nodes
            FROM keywords
            GROUP BY keyword
            HAVING COUNT(*) >= 2
        """)
        
        clusters = []
        for row in cursor.fetchall():
            keyword, nodes_str = row
            nodes = nodes_str.split(',')
            if len(nodes) >= 2:
                clusters.append({"keyword": keyword, "nodes": nodes, "size": len(nodes)})
        
        conn.close()
        
        clusters.sort(key=lambda x: x["size"], reverse=True)
        return clusters[:10]
    
    def export_graph(self, format: str = "json") -> str:
        """导出图谱"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, content, category FROM nodes")
        nodes = [{"id": r[0], "content": r[1][:100], "category": r[2]} for r in cursor.fetchall()]
        
        cursor.execute("SELECT source, target, relation, weight FROM edges")
        edges = [{"source": r[0], "target": r[1], "relation": r[2], "weight": r[3]} for r in cursor.fetchall()]
        
        conn.close()
        
        if format == "json":
            return json.dumps({"nodes": nodes, "edges": edges}, indent=2, ensure_ascii=False)
        
        return json.dumps({"nodes": nodes, "edges": edges})

if __name__ == "__main__":
    import sys
    
    kg = KnowledgeGraph()
    
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        nodes, edges = kg.build_graph()
        print(f"✅ Built graph: {nodes} nodes, {edges} edges")
    else:
        nodes, edges = kg.build_graph()
        print(f"✅ Graph: {nodes} nodes, {edges} edges")