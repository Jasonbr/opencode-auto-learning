#!/usr/bin/env python3
"""OpenCode Session Exporter V2

从 OpenCode 数据库导出会话到 Markdown 文件。
支持从 part 表正确读取消息内容。
"""
import sqlite3
import json
import re
from pathlib import Path
from datetime import datetime


class SessionExporter:
    def __init__(self):
        self.db_path = Path.home() / ".local/share/opencode/opencode-.db"
        self.output_dir = Path.home() / ".config/opencode/memory/sessions"
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def get_db_connection(self):
        if not self.db_path.exists():
            raise FileNotFoundError(f"数据库不存在: {self.db_path}")
        return sqlite3.connect(self.db_path)
    
    def export_sessions(self):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        
        # 获取所有会话
        cursor.execute("""
            SELECT s.id, s.title, s.created_at, s.updated_at, s.message_count
            FROM session s
            ORDER BY s.updated_at DESC
        """)
        
        sessions = cursor.fetchall()
        exported = 0
        
        for session in sessions:
            session_id, title, created_at, updated_at, msg_count = session
            
            # 获取会话消息 - 从 part 表读取
            cursor.execute("""
                SELECT m.id, m.created_at, m.role, p.data
                FROM message m
                JOIN part p ON p.message_id = m.id
                WHERE m.session_id = ?
                ORDER BY m.created_at ASC
            """, (session_id,))
            
            messages = cursor.fetchall()
            
            if not messages:
                continue
            
            # 生成文件名
            safe_title = re.sub(r'[^\w\u4e00-\u9fff_-]', '_', title or 'untitled')[:30]
            date_str = datetime.fromisoformat(updated_at.replace('Z', '+00:00')).strftime('%Y%m%d')
            filename = f"{date_str}_ses_{session_id[:4]}_{safe_title}.md"
            filepath = self.output_dir / filename
            
            # 写入会话内容
            content = f"""# {title or 'Untitled Session'}

- **Session ID**: `{session_id}`
- **Created**: {created_at}
- **Updated**: {updated_at}
- **Messages**: {len(messages)}

---

"""
            
            for msg_id, msg_time, role, part_data in messages:
                try:
                    part_json = json.loads(part_data)
                    if part_json.get('type') == 'text' and 'text' in part_json:
                        msg_text = part_json['text']
                        # 截断长消息
                        if len(msg_text) > 2000:
                            msg_text = msg_text[:2000] + "\n\n... (truncated)"
                        
                        role_label = "🧑‍💻 USER" if role == "user" else "🤖 ASSISTANT"
                        content += f"### {role_label}\n\n{msg_text}\n\n---\n\n"
                except json.JSONDecodeError:
                    continue
            
            filepath.write_text(content, encoding='utf-8')
            exported += 1
        
        conn.close()
        print(f"✅ 导出 {exported} 个会话到 {self.output_dir}")
        return exported


if __name__ == "__main__":
    exporter = SessionExporter()
    exporter.export_sessions()
