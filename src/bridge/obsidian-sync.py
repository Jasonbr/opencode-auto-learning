#!/usr/bin/env python3
"""
Obsidian Vault 同步工具
自动将记忆同步到 Obsidian 知识库
"""

import json
import sqlite3
import os
from datetime import datetime
from pathlib import Path

class ObsidianSync:
    def __init__(self):
        self.vault_path = Path.home() / "Documents/Obsidian Vault/Knowledge"
        self.mem0_db = Path.home() / ".mem0" / "local_memory.db"
    
    def sync_memories_to_obsidian(self):
        """同步记忆到 Obsidian"""
        if not self.mem0_db.exists():
            print("⚠️  Mem0 DB not found")
            return
        
        conn = sqlite3.connect(self.mem0_db)
        cursor = conn.cursor()
        
        # 获取今天的记忆
        today = datetime.now().strftime("%Y-%m-%d")
        cursor.execute("""
            SELECT category, content, metadata, created_at
            FROM memories
            WHERE date(created_at) = date('now')
            ORDER BY category, created_at
        """)
        
        results = cursor.fetchall()
        conn.close()
        
        if not results:
            print("ℹ️  No memories to sync today")
            return
        
        # 按分类分组
        by_category = {}
        for row in results:
            cat = row[0]
            if cat not in by_category:
                by_category[cat] = []
            by_category[cat].append({
                "content": row[1],
                "metadata": json.loads(row[2]) if row[2] else {},
                "created_at": row[3]
            })
        
        # 创建每日同步笔记
        sync_dir = self.vault_path / "Daily Sync"
        sync_dir.mkdir(exist_ok=True)
        
        note_path = sync_dir / f"{today}.md"
        
        with open(note_path, 'w', encoding='utf-8') as f:
            f.write(f"# Daily Memory Sync - {today}\\n\\n")
            
            for category, items in by_category.items():
                f.write(f"\\n## {category}\\n\\n")
                for item in items:
                    time = datetime.fromisoformat(item['created_at']).strftime('%H:%M')
                    f.write(f"- **{time}** {item['content']}\\n")
        
        print(f"✅ Synced {len(results)} memories to {note_path}")
    
    def create_session_summary(self, title: str, content: str):
        """创建会话总结"""
        today = datetime.now().strftime("%Y-%m-%d")
        session_dir = self.vault_path / "Session Summaries"
        session_dir.mkdir(exist_ok=True)
        
        note_path = session_dir / f"{today}.md"
        
        with open(note_path, 'a', encoding='utf-8') as f:
            f.write(f"\\n## {datetime.now().strftime('%H:%M')} - {title}\\n\\n")
            f.write(content)
            f.write("\\n\\n---\\n")
        
        print(f"✅ Session summary saved to {note_path}")

if __name__ == "__main__":
    import sys
    
    sync = ObsidianSync()
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "sync":
            sync.sync_memories_to_obsidian()
        elif sys.argv[1] == "summary" and len(sys.argv) > 3:
            sync.create_session_summary(sys.argv[2], sys.argv[3])
        else:
            print("Usage: obsidian-sync.py [sync|summary <title> <content>]")
    else:
        sync.sync_memories_to_obsidian()
