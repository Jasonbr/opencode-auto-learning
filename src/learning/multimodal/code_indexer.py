#!/usr/bin/env python3
"""
代码片段索引模块
"""

import sqlite3
import json
import hashlib
from pathlib import Path
from datetime import datetime

class CodeIndexer:
    def __init__(self, user_id="default"):
        self.user_id = user_id
        self.mem0_db = Path.home() / ".mem0" / "local_memory.db"
    
    def index_file(self, file_path, description=""):
        """索引代码文件"""
        file_path = Path(file_path)
        
        if not file_path.exists():
            return {"error": "File not found"}
        
        try:
            code = file_path.read_text(encoding='utf-8')
            language = self._detect_language(file_path.suffix)
            
            # 保存到数据库
            result = self._save_to_memory(code, language, description or f"Code from {file_path.name}")
            
            return {
                "success": True,
                "memory_id": result.get("memory_id"),
                "language": language,
                "lines": len(code.split('\n'))
            }
        except Exception as e:
            return {"error": str(e)}
    
    def _detect_language(self, ext):
        """检测语言"""
        mapping = {
            '.py': 'python', '.js': 'javascript', '.ts': 'typescript',
            '.sh': 'bash', '.go': 'go', '.rs': 'rust', '.sql': 'sql',
            '.yml': 'yaml', '.yaml': 'yaml', '.json': 'json', '.md': 'markdown'
        }
        return mapping.get(ext.lower(), 'text')
    
    def _save_to_memory(self, code, language, description):
        """保存到记忆"""
        if not self.mem0_db.exists():
            return {"error": "Database not found"}
        
        conn = sqlite3.connect(self.mem0_db)
        cursor = conn.cursor()
        
        content = f"[CODE] {language}\n{description}\n\n{code[:500]}"
        
        cursor.execute("""
            INSERT INTO memories (user_id, content, category, metadata, created_at)
            VALUES (?, ?, ?, ?, ?)
        """, (
            self.user_id,
            content,
            "code",
            json.dumps({"type": "code", "language": language, "description": description}),
            datetime.now().isoformat()
        ))
        
        memory_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return {"memory_id": memory_id}
    
    def search_code(self, query, language=None):
        """搜索代码"""
        if not self.mem0_db.exists():
            return []
        
        conn = sqlite3.connect(self.mem0_db)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, content, metadata, created_at
            FROM memories
            WHERE category = 'code'
            AND content LIKE ?
            ORDER BY created_at DESC
            LIMIT 10
        """, (f"%{query}%",))
        
        results = []
        for row in cursor.fetchall():
            metadata = json.loads(row[2]) if row[2] else {}
            results.append({
                "id": row[0],
                "content": row[1][:100],
                "language": metadata.get("language", "unknown"),
                "created_at": row[3]
            })
        
        conn.close()
        return results

def main():
    import sys
    
    indexer = CodeIndexer()
    
    if len(sys.argv) < 2:
        print("Usage: code_indexer.py <command> [args]")
        print("Commands: index <file> [desc], search <query>")
        return
    
    command = sys.argv[1]
    
    if command == "index":
        file_path = sys.argv[2]
        description = sys.argv[3] if len(sys.argv) > 3 else ""
        result = indexer.index_file(file_path, description)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif command == "search":
        query = sys.argv[2]
        results = indexer.search_code(query)
        print(json.dumps(results, indent=2, ensure_ascii=False))
    
    else:
        print(f"Unknown command: {command}")

if __name__ == "__main__":
    main()
