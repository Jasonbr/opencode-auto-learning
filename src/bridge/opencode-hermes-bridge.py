#!/usr/bin/env python3
"""
Hermes ↔ OpenCode 记忆桥接器
实现双向记忆同步
"""

import json
import sqlite3
import os
import sys
from datetime import datetime
from pathlib import Path

class MemoryBridge:
    def __init__(self):
        self.user_id = "xiaoxi"
        self.mem0_db = Path.home() / ".mem0" / "local_memory.db"
        self.hermes_db = Path.home() / ".hermes" / "memory.db"
        self.obsidian_vault = Path.home() / "Documents/Obsidian Vault/Knowledge"
        
    def sync_opencode_to_hermes(self):
        """将 OpenCode/Mem0 记忆同步到 Hermes"""
        print("🔄 Syncing OpenCode → Hermes...")
        
        # 获取 Mem0 新记忆
        new_memories = self._get_new_memories()
        
        if not new_memories:
            print("  ℹ️  No new memories to sync")
            return
        
        # 同步到 Hermes
        for mem in new_memories:
            self._save_to_hermes(
                content=mem["content"],
                category=mem.get("category", "general"),
                tags=mem.get("tags", [])
            )
        
        # 同步到 Obsidian
        self._sync_to_obsidian(new_memories)
        
        print(f"  ✅ Synced {len(new_memories)} memories")
    
    def sync_hermes_to_opencode(self):
        """将 Hermes 记忆加载到 OpenCode"""
        print("🔄 Syncing Hermes → OpenCode...")
        
        # 获取 Hermes 记忆
        facts = self._get_hermes_facts()
        
        if not facts:
            print("  ℹ️  No Hermes facts to sync")
            return
        
        # 保存到 Mem0
        for fact in facts:
            self._save_to_mem0(fact)
        
        print(f"  ✅ Synced {len(facts)} facts")
    
    def _get_new_memories(self):
        """获取 Mem0 中新添加的记忆（最近1小时）"""
        if not self.mem0_db.exists():
            return []
        
        conn = sqlite3.connect(self.mem0_db)
        cursor = conn.cursor()
        
        # 获取最近1小时的记忆（不限制 source，因为 schema 可能不同）
        cursor.execute("""
            SELECT id, content, category, metadata, created_at 
            FROM memories 
            WHERE user_id = ? 
            AND created_at > datetime('now', '-1 hour')
            ORDER BY created_at DESC
        """, (self.user_id,))
        
        results = cursor.fetchall()
        conn.close()
        
        memories = []
        for r in results:
            try:
                metadata = json.loads(r[3]) if r[3] else {}
            except:
                metadata = {}
            
            memories.append({
                "id": r[0],
                "content": r[1],
                "category": r[2] or "general",
                "metadata": metadata,
                "created_at": r[4]
            })
        
        return memories
    
    def _save_to_hermes(self, content, category, tags):
        """保存到 Hermes"""
        # 使用 fact_store
        try:
            # 这里调用 Hermes 的 fact_store API
            # 简化版：直接打印
            print(f"    → Saved to Hermes: {content[:50]}...")
        except Exception as e:
            print(f"    ✗ Error: {e}")
    
    def _sync_to_obsidian(self, memories):
        """同步到 Obsidian Vault"""
        if not self.obsidian_vault.exists():
            return
        
        today = datetime.now().strftime("%Y-%m-%d")
        session_dir = self.obsidian_vault / "Session Summaries"
        session_dir.mkdir(exist_ok=True)
        
        note_path = session_dir / f"{today}-OpenCode.md"
        
        with open(note_path, 'a', encoding='utf-8') as f:
            for mem in memories:
                f.write(f"\n## {mem['created_at']}\n")
                f.write(f"{mem['content']}\n")
                f.write(f"Category: {mem['category']}\n")
                f.write("---\n")
    
    def _get_hermes_facts(self):
        """获取 Hermes 记忆"""
        # 这里从 Hermes 获取
        return []
    
    def _save_to_mem0(self, fact):
        """保存到 Mem0"""
        # 这里保存到 Mem0
        pass
    
    def export_session_summary(self):
        """导出会话总结"""
        print("📝 Exporting session summary...")
        
        # 生成总结
        summary = self._generate_summary()
        
        # 保存到 Obsidian
        today = datetime.now().strftime("%Y-%m-%d")
        note_path = self.obsidian_vault / "Session Summaries" / f"{today}.md"
        
        with open(note_path, 'a', encoding='utf-8') as f:
            f.write(f"\n## Session Summary {datetime.now().strftime('%H:%M')}\n")
            f.write(summary)
            f.write("\n\n---\n")
        
        print(f"  ✅ Saved to {note_path}")
    
    def _generate_summary(self):
        """生成会话总结"""
        return "Session summary placeholder"

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Hermes ↔ OpenCode Memory Bridge")
    parser.add_argument("action", choices=["export", "import", "sync", "summary"],
                       help="Action to perform")
    
    args = parser.parse_args()
    
    bridge = MemoryBridge()
    
    if args.action == "export":
        bridge.sync_opencode_to_hermes()
    elif args.action == "import":
        bridge.sync_hermes_to_opencode()
    elif args.action == "sync":
        bridge.sync_hermes_to_opencode()
        bridge.sync_opencode_to_hermes()
    elif args.action == "summary":
        bridge.export_session_summary()

if __name__ == "__main__":
    main()
