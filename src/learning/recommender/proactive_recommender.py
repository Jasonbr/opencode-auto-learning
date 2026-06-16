#!/usr/bin/env python3
"""
主动推荐系统
分析上下文并主动推送相关知识
"""

import sqlite3
import json
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import hashlib

class Recommender:
    def __init__(self, user_id="default"):
        self.user_id = user_id
        self.vector_db = Path.home() / ".mem0" / "vector_memory.db"
        self.graph_db = Path.home() / ".mem0" / "knowledge_graph.db"
        self.mem0_db = Path.home() / ".mem0" / "local_memory.db"
        
    def analyze_context(self, text: str) -> Dict:
        """分析文本上下文"""
        # 提取关键词
        keywords = self._extract_keywords(text)
        
        # 推断意图
        intent = self._infer_intent(text)
        
        # 识别实体
        entities = self._extract_entities(text)
        
        return {
            "keywords": keywords,
            "intent": intent,
            "entities": entities
        }
    
    def _extract_keywords(self, text: str) -> List[str]:
        """提取关键词"""
        # 简单实现：提取技术词汇
        tech_keywords = [
            "docker", "kubernetes", "k8s", "github", "git",
            "python", "javascript", "typescript", "react", "vue",
            "database", "api", "mcp", "memory", "sync",
            "deployment", "ci/cd", "testing", "debug"
        ]
        
        text_lower = text.lower()
        found = []
        for keyword in tech_keywords:
            if keyword in text_lower:
                found.append(keyword)
        
        # 也提取大写词汇（可能是专有名词）
        import re
        capitals = re.findall(r'\b[A-Z][a-zA-Z]+\b', text)
        found.extend([c for c in capitals if len(c) > 2])
        
        return list(set(found))[:10]
    
    def _infer_intent(self, text: str) -> str:
        """推断用户意图"""
        text_lower = text.lower()
        
        patterns = {
            "implement": ["implement", "create", "build", "develop"],
            "fix": ["fix", "bug", "error", "issue", "problem"],
            "learn": ["learn", "understand", "how to", "what is"],
            "optimize": ["optimize", "improve", "performance", "speed"],
            "deploy": ["deploy", "release", "publish", "ship"],
            "config": ["config", "setup", "install", "configure"]
        }
        
        for intent, keywords in patterns.items():
            if any(k in text_lower for k in keywords):
                return intent
        
        return "general"
    
    def _extract_entities(self, text: str) -> List[str]:
        """提取命名实体"""
        import re
        
        # 提取可能的文件名、路径、URL
        entities = []
        
        # 文件名
        files = re.findall(r'\b\w+\.(py|js|ts|json|yaml|yml|md|sh)\b', text)
        entities.extend(files)
        
        # 路径
        paths = re.findall(r'[~/]\w+[/\w+]*', text)
        entities.extend(paths)
        
        return entities[:5]
    
    def recommend(self, context: str, limit: int = 5) -> List[Dict]:
        """基于上下文推荐记忆"""
        analysis = self.analyze_context(context)
        
        recommendations = []
        
        # 1. 关键词匹配
        keyword_results = self._search_by_keywords(analysis["keywords"], limit)
        recommendations.extend(keyword_results)
        
        # 2. 意图匹配
        intent_results = self._search_by_intent(analysis["intent"], limit)
        recommendations.extend(intent_results)
        
        # 3. 语义相似度
        semantic_results = self._semantic_search(context, limit)
        recommendations.extend(semantic_results)
        
        # 去重和排序
        unique_recommendations = self._deduplicate_and_rank(recommendations)
        
        return unique_recommendations[:limit]
    
    def _search_by_keywords(self, keywords: List[str], limit: int) -> List[Dict]:
        """按关键词搜索"""
        if not keywords:
            return []
        
        if not self.mem0_db.exists():
            return []
        
        conn = sqlite3.connect(self.mem0_db)
        cursor = conn.cursor()
        
        results = []
        
        # 查找包含关键词的记忆
        for keyword in keywords:
            cursor.execute("""
                SELECT id, content, category, created_at
                FROM memories
                WHERE content LIKE ?
                ORDER BY created_at DESC
                LIMIT ?
            """, (f"%{keyword}%", limit))
            
            for row in cursor.fetchall():
                results.append({
                    "id": row[0],
                    "content": row[1][:200],
                    "category": row[2],
                    "created_at": row[3],
                    "match_type": "keyword",
                    "match_score": 0.8
                })
        
        conn.close()
        return results
    
    def _search_by_intent(self, intent: str, limit: int) -> List[Dict]:
        """按意图搜索"""
        if not self.mem0_db.exists():
            return []
        
        conn = sqlite3.connect(self.mem0_db)
        cursor = conn.cursor()
        
        # 查找相同意图的历史记忆
        intent_categories = {
            "implement": ["decision", "architecture"],
            "fix": ["error-solution", "debugging"],
            "learn": ["learning", "tutorial"],
            "optimize": ["performance", "optimization"],
            "deploy": ["deployment", "devops"],
            "config": ["configuration", "setup"]
        }
        
        categories = intent_categories.get(intent, [])
        if not categories:
            return []
        
        placeholders = ",".join(["?"] * len(categories))
        query = f"""
            SELECT id, content, category, created_at
            FROM memories
            WHERE category IN ({placeholders})
            ORDER BY created_at DESC
            LIMIT ?
        """
        
        cursor.execute(query, categories + [limit])
        
        results = []
        for row in cursor.fetchall():
            results.append({
                "id": row[0],
                "content": row[1][:200],
                "category": row[2],
                "created_at": row[3],
                "match_type": "intent",
                "match_score": 0.7
            })
        
        conn.close()
        return results
    
    def _semantic_search(self, query: str, limit: int) -> List[Dict]:
        """语义搜索"""
        try:
            # 简化实现：使用关键词搜索代替
            return []
        except Exception as e:
            print(f"Semantic search error: {e}")
            return []
    
    def _deduplicate_and_rank(self, recommendations: List[Dict]) -> List[Dict]:
        """去重和排序"""
        seen = set()
        unique = []
        
        for rec in recommendations:
            rec_id = rec.get("id")
            if rec_id and rec_id not in seen:
                seen.add(rec_id)
                unique.append(rec)
        
        # 按匹配分数排序
        unique.sort(key=lambda x: x.get("match_score", 0), reverse=True)
        
        return unique
    
    def get_proactive_recommendations(self, session_duration_minutes: int = 0) -> List[Dict]:
        """主动推荐（基于会话时长）"""
        if session_duration_minutes < 10:
            return []
        
        # 长时间会话，推荐相关知识
        recent_context = self._get_recent_context()
        
        if recent_context:
            return self.recommend(recent_context, limit=3)
        
        return []
    
    def _get_recent_context(self) -> str:
        """获取最近的活动上下文"""
        # 简化实现：获取最近的记忆内容
        if not self.mem0_db.exists():
            return ""
        
        conn = sqlite3.connect(self.mem0_db)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT content FROM memories
            ORDER BY created_at DESC
            LIMIT 3
        """)
        
        contents = [row[0] for row in cursor.fetchall()]
        conn.close()
        
        return " ".join(contents)

def main():
    import sys
    
    recommender = Recommender()
    
    if len(sys.argv) < 2:
        print("Usage: recommender.py <command> [args]")
        print("Commands:")
        print("  recommend <text>    Get recommendations for text")
        print("  analyze <text>      Analyze context")
        print("  proactive           Get proactive recommendations")
        return
    
    command = sys.argv[1]
    
    if command == "recommend":
        text = " ".join(sys.argv[2:])
        results = recommender.recommend(text)
        print(json.dumps(results, indent=2, ensure_ascii=False))
    
    elif command == "analyze":
        text = " ".join(sys.argv[2:])
        analysis = recommender.analyze_context(text)
        print(json.dumps(analysis, indent=2, ensure_ascii=False))
    
    elif command == "proactive":
        results = recommender.get_proactive_recommendations(session_duration_minutes=30)
        print(json.dumps(results, indent=2, ensure_ascii=False))
    
    else:
        print(f"Unknown command: {command}")

if __name__ == "__main__":
    main()