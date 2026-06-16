#!/usr/bin/env python3
"""
智能总结生成系统
自动分析会话并生成高质量总结
"""

import sqlite3
import json
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
import re

@dataclass
class SessionSummary:
    """会话总结"""
    title: str
    executive_summary: str
    key_decisions: List[str]
    learnings: List[str]
    action_items: List[str]
    technical_details: List[str]
    duration_minutes: int
    memory_count: int
    generated_at: str

class SessionAnalyzer:
    """会话分析器"""
    
    def __init__(self, user_id="default"):
        self.user_id = user_id
        self.mem0_db = Path.home() / ".mem0" / "local_memory.db"
        
    def analyze_session(self, start_time: Optional[datetime] = None, 
                       end_time: Optional[datetime] = None) -> SessionSummary:
        """分析会话并生成总结"""
        
        # 1. 获取会话记忆
        memories = self._get_session_memories(start_time, end_time)
        
        if not memories:
            return SessionSummary(
                title="Empty Session",
                executive_summary="No memories found for this session",
                key_decisions=[],
                learnings=[],
                action_items=[],
                technical_details=[],
                duration_minutes=0,
                memory_count=0,
                generated_at=datetime.now().isoformat()
            )
        
        # 2. 提取关键信息
        key_decisions = self._extract_decisions(memories)
        learnings = self._extract_learnings(memories)
        action_items = self._extract_action_items(memories)
        technical_details = self._extract_technical_details(memories)
        
        # 3. 生成执行摘要
        executive_summary = self._generate_executive_summary(memories)
        
        # 4. 生成标题
        title = self._generate_title(memories)
        
        # 5. 计算会话时长
        duration = self._calculate_duration(memories)
        
        return SessionSummary(
            title=title,
            executive_summary=executive_summary,
            key_decisions=key_decisions,
            learnings=learnings,
            action_items=action_items,
            technical_details=technical_details,
            duration_minutes=duration,
            memory_count=len(memories),
            generated_at=datetime.now().isoformat()
        )
    
    def _get_session_memories(self, start_time: Optional[datetime], 
                             end_time: Optional[datetime]) -> List[Dict]:
        """获取会话期间的记忆"""
        if not self.mem0_db.exists():
            return []
        
        conn = sqlite3.connect(self.mem0_db)
        cursor = conn.cursor()
        
        # 默认获取最近 24 小时的记忆
        if not start_time:
            start_time = datetime.now() - timedelta(hours=24)
        if not end_time:
            end_time = datetime.now()
        
        cursor.execute("""
            SELECT id, content, category, metadata, created_at
            FROM memories
            WHERE user_id = ?
            AND created_at BETWEEN ? AND ?
            ORDER BY created_at ASC
        """, (self.user_id, start_time.isoformat(), end_time.isoformat()))
        
        memories = []
        for row in cursor.fetchall():
            memories.append({
                "id": row[0],
                "content": row[1],
                "category": row[2],
                "metadata": json.loads(row[3]) if row[3] else {},
                "created_at": row[4]
            })
        
        conn.close()
        return memories
    
    def _extract_decisions(self, memories: List[Dict]) -> List[str]:
        """提取关键决策"""
        decisions = []
        
        decision_patterns = [
            r"决定[使采用]\s*[:：]\s*(.+?)(?:\n|$)",
            r"选择[使采用]\s*[:：]\s*(.+?)(?:\n|$)",
            r"采用\s*[:：]\s*(.+?)(?:\n|$)",
            r"使用\s*[:：]\s*(.+?)(?:\n|$)",
            r"方案[：:]\s*(.+?)(?:\n|$)"
        ]
        
        for memory in memories:
            content = memory["content"]
            category = memory.get("category", "")
            
            # 直接标记为 decision 的记忆
            if category == "decision":
                decisions.append(content[:200])
                continue
            
            # 从内容中提取
            for pattern in decision_patterns:
                matches = re.findall(pattern, content)
                decisions.extend([m.strip()[:200] for m in matches])
        
        return list(set(decisions))[:10]  # 去重，最多10条
    
    def _extract_learnings(self, memories: List[Dict]) -> List[str]:
        """提取学习点"""
        learnings = []
        
        learning_patterns = [
            r"发现\s*[:：]\s*(.+?)(?:\n|$)",
            r"学到\s*[:：]\s*(.+?)(?:\n|$)",
            r"理解\s*[:：]\s*(.+?)(?:\n|$)",
            r"注意\s*[:：]\s*(.+?)(?:\n|$)",
            r"关键\s*[:：]\s*(.+?)(?:\n|$)"
        ]
        
        for memory in memories:
            content = memory["content"]
            category = memory.get("category", "")
            
            if category == "learning":
                learnings.append(content[:200])
                continue
            
            for pattern in learning_patterns:
                matches = re.findall(pattern, content)
                learnings.extend([m.strip()[:200] for m in matches])
        
        return list(set(learnings))[:10]
    
    def _extract_action_items(self, memories: List[Dict]) -> List[str]:
        """提取行动项"""
        action_items = []
        
        action_patterns = [
            r"TODO[:：]\s*(.+?)(?:\n|$)",
            r"待办[:：]\s*(.+?)(?:\n|$)",
            r"下一步[:：]\s*(.+?)(?:\n|$)",
            r"需要\s*(.+?)(?:\n|$)",
            r"应该\s*(.+?)(?:\n|$)"
        ]
        
        for memory in memories:
            content = memory["content"]
            
            for pattern in action_patterns:
                matches = re.findall(pattern, content)
                action_items.extend([m.strip()[:200] for m in matches])
        
        return list(set(action_items))[:10]
    
    def _extract_technical_details(self, memories: List[Dict]) -> List[str]:
        """提取技术细节"""
        technical = []
        
        # 技术相关的分类
        tech_categories = ["technical", "implementation", "configuration", "debugging"]
        
        for memory in memories:
            category = memory.get("category", "")
            content = memory["content"]
            
            if category in tech_categories:
                technical.append(content[:300])
        
        return technical[:10]
    
    def _generate_executive_summary(self, memories: List[Dict]) -> str:
        """生成执行摘要"""
        if not memories:
            return "No activities recorded"
        
        # 按分类统计
        categories = {}
        for m in memories:
            cat = m.get("category", "general")
            categories[cat] = categories.get(cat, 0) + 1
        
        # 生成摘要
        total = len(memories)
        summary_parts = [f"Session contains {total} memories"]
        
        if categories:
            top_cats = sorted(categories.items(), key=lambda x: x[1], reverse=True)[:3]
            cat_str = ", ".join([f"{k}({v})" for k, v in top_cats])
            summary_parts.append(f"covering {cat_str}")
        
        # 添加时间范围
        times = [m["created_at"] for m in memories if m.get("created_at")]
        if times:
            first = min(times)
            last = max(times)
            summary_parts.append(f"from {first[:10]} to {last[:10]}")
        
        return " ".join(summary_parts)
    
    def _generate_title(self, memories: List[Dict]) -> str:
        """生成会话标题"""
        if not memories:
            return "Empty Session"
        
        # 提取关键词
        all_content = " ".join([m["content"] for m in memories])
        keywords = self._extract_keywords(all_content)
        
        if keywords:
            return f"Session: {', '.join(keywords[:3])}"
        
        return f"Session with {len(memories)} memories"
    
    def _extract_keywords(self, text: str) -> List[str]:
        """提取关键词"""
        tech_keywords = [
            "docker", "kubernetes", "k8s", "github", "git",
            "python", "javascript", "typescript", "react", "vue",
            "database", "api", "mcp", "memory", "sync",
            "deployment", "ci/cd", "testing", "debug",
            "OpenCode", "Hermes", "Mem0"
        ]
        
        text_lower = text.lower()
        found = []
        for keyword in tech_keywords:
            if keyword.lower() in text_lower:
                found.append(keyword)
        
        return list(set(found))
    
    def _calculate_duration(self, memories: List[Dict]) -> int:
        """计算会话时长（分钟）"""
        if not memories:
            return 0
        
        times = []
        for m in memories:
            if m.get("created_at"):
                try:
                    t = datetime.fromisoformat(m["created_at"])
                    times.append(t)
                except:
                    pass
        
        if len(times) < 2:
            return 0
        
        duration = max(times) - min(times)
        return int(duration.total_seconds() / 60)

class SummaryFormatter:
    """总结格式化器"""
    
    def to_markdown(self, summary: SessionSummary) -> str:
        """转换为 Markdown"""
        lines = [
            f"# {summary.title}",
            "",
            f"**Generated**: {summary.generated_at}",
            f"**Duration**: {summary.duration_minutes} minutes",
            f"**Memories**: {summary.memory_count}",
            "",
            "## Executive Summary",
            "",
            summary.executive_summary,
            "",
        ]
        
        if summary.key_decisions:
            lines.extend([
                "## Key Decisions",
                ""
            ])
            for i, decision in enumerate(summary.key_decisions, 1):
                lines.append(f"{i}. {decision}")
            lines.append("")
        
        if summary.learnings:
            lines.extend([
                "## Key Learnings",
                ""
            ])
            for i, learning in enumerate(summary.learnings, 1):
                lines.append(f"{i}. {learning}")
            lines.append("")
        
        if summary.action_items:
            lines.extend([
                "## Action Items",
                ""
            ])
            for i, item in enumerate(summary.action_items, 1):
                lines.append(f"- [ ] {item}")
            lines.append("")
        
        if summary.technical_details:
            lines.extend([
                "## Technical Details",
                ""
            ])
            for detail in summary.technical_details[:3]:
                lines.append(f"```")
                lines.append(detail[:500])
                lines.append(f"```")
                lines.append("")
        
        return "\n".join(lines)
    
    def to_json(self, summary: SessionSummary) -> str:
        """转换为 JSON"""
        return json.dumps({
            "title": summary.title,
            "executive_summary": summary.executive_summary,
            "key_decisions": summary.key_decisions,
            "learnings": summary.learnings,
            "action_items": summary.action_items,
            "technical_details": summary.technical_details,
            "duration_minutes": summary.duration_minutes,
            "memory_count": summary.memory_count,
            "generated_at": summary.generated_at
        }, indent=2, ensure_ascii=False)
    
    def to_text(self, summary: SessionSummary) -> str:
        """转换为纯文本"""
        lines = [
            f"Session Summary: {summary.title}",
            f"Duration: {summary.duration_minutes} minutes | Memories: {summary.memory_count}",
            "",
            "SUMMARY:",
            summary.executive_summary,
            ""
        ]
        
        if summary.key_decisions:
            lines.extend(["DECISIONS:", ""])
            for decision in summary.key_decisions:
                lines.append(f"- {decision}")
            lines.append("")
        
        if summary.action_items:
            lines.extend(["ACTIONS:", ""])
            for item in summary.action_items:
                lines.append(f"[ ] {item}")
            lines.append("")
        
        return "\n".join(lines)

def main():
    import sys
    
    analyzer = SessionAnalyzer()
    formatter = SummaryFormatter()
    
    if len(sys.argv) < 2:
        print("Usage: session_summary.py <command> [args]")
        print("Commands:")
        print("  generate [hours]     Generate summary for last N hours (default: 24)")
        print("  daily                Generate daily summary")
        print("  weekly               Generate weekly summary")
        print("  export <format>      Export summary (md/json/text)")
        return
    
    command = sys.argv[1]
    
    if command == "generate":
        hours = int(sys.argv[2]) if len(sys.argv) > 2 else 24
        start_time = datetime.now() - timedelta(hours=hours)
        
        print(f"📊 Generating summary for last {hours} hours...")
        summary = analyzer.analyze_session(start_time=start_time)
        
        print(formatter.to_markdown(summary))
    
    elif command == "daily":
        start_time = datetime.now() - timedelta(days=1)
        
        print("📊 Generating daily summary...")
        summary = analyzer.analyze_session(start_time=start_time)
        
        # 保存到 Obsidian
        vault_path = Path.home() / "Documents/Obsidian Vault/Knowledge/Daily Summary"
        vault_path.mkdir(parents=True, exist_ok=True)
        
        filename = f"{datetime.now().strftime('%Y-%m-%d')}-summary.md"
        filepath = vault_path / filename
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(formatter.to_markdown(summary))
        
        print(f"✅ Saved to: {filepath}")
        print("\n" + formatter.to_text(summary))
    
    elif command == "weekly":
        start_time = datetime.now() - timedelta(weeks=1)
        
        print("📊 Generating weekly summary...")
        summary = analyzer.analyze_session(start_time=start_time)
        
        print(formatter.to_markdown(summary))
    
    elif command == "export":
        format_type = sys.argv[2] if len(sys.argv) > 2 else "md"
        summary = analyzer.analyze_session()
        
        if format_type == "json":
            print(formatter.to_json(summary))
        elif format_type == "text":
            print(formatter.to_text(summary))
        else:
            print(formatter.to_markdown(summary))
    
    else:
        print(f"Unknown command: {command}")

if __name__ == "__main__":
    main()