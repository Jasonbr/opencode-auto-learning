#!/usr/bin/env python3
"""OpenCode Memory Extractor V2

智能提取会话中的知识点，生成结构化记忆。
"""
import re
import hashlib
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional


class MemoryExtractor:
    def __init__(self):
        self.sessions_dir = Path.home() / ".config/opencode/memory/sessions"
        self.memory_dir = Path.home() / ".config/opencode/memory/user"
        self.memory_dir.mkdir(parents=True, exist_ok=True)
        
        self.extractors = [
            self._extract_code,
            self._extract_decisions,
            self._extract_errors,
            self._extract_patterns,
            self._extract_learnings
        ]
    
    def _extract_code(self, text: str, session: str) -> Optional[Dict]:
        code_blocks = re.findall(r'```(?:bash|shell|sh|python|js|ts)?\n(.*?)\n```', text, re.DOTALL)
        if code_blocks and len(code_blocks[0]) > 20:
            return {
                "type": "code",
                "content": code_blocks[0][:500],
                "confidence": 0.8
            }
        return None
    
    def _extract_decisions(self, text: str, session: str) -> Optional[Dict]:
        patterns = [r'决定.*?(?:\n|$)', r'方案.*?(?:\n|$)', r'选择.*?(?:\n|$)']
        for pattern in patterns:
            match = re.search(pattern, text, re.MULTILINE)
            if match and len(match.group()) > 10:
                return {
                    "type": "decision",
                    "content": match.group(),
                    "confidence": 0.7
                }
        return None
    
    def _extract_errors(self, text: str, session: str) -> Optional[Dict]:
        error_patterns = [r'Error.*?(?:\n|$)', r'Failed.*?(?:\n|$)', r'解决.*?(?:\n|$)']
        for pattern in error_patterns:
            match = re.search(pattern, text, re.MULTILINE)
            if match:
                return {
                    "type": "error-solution",
                    "content": match.group(),
                    "confidence": 0.75
                }
        return None
    
    def _extract_patterns(self, text: str, session: str) -> Optional[Dict]:
        if '模式' in text or 'pattern' in text.lower():
            sentences = [s for s in text.split('。') if '模式' in s or 'pattern' in s.lower()]
            if sentences:
                return {
                    "type": "pattern",
                    "content": sentences[0][:200],
                    "confidence": 0.6
                }
        return None
    
    def _extract_learnings(self, text: str, session: str) -> Optional[Dict]:
        keywords = ['理解', '明白', '发现', '意识到', '学会了', '注意']
        sentences = text.split('。')
        for sent in sentences:
            if any(kw in sent for kw in keywords) and len(sent) > 15:
                return {
                    "type": "learning",
                    "content": sent.strip()[:300],
                    "confidence": 0.7
                }
        return None
    
    def process_session(self, session_file: Path) -> List[Dict]:
        content = session_file.read_text(encoding='utf-8')
        memories = []
        seen = set()
        
        for extractor in self.extractors:
            try:
                memory = extractor(content, session_file.name)
                if memory:
                    # 去重
                    content_hash = hashlib.md5(memory['content'][:100].encode()).hexdigest()[:12]
                    if content_hash not in seen:
                        seen.add(content_hash)
                        memory.update({
                            "file": session_file.name,
                            "extracted_at": datetime.now().isoformat()
                        })
                        memories.append(memory)
            except Exception:
                continue
        
        return memories
    
    def save_memory(self, memory: Dict):
        mem_type = memory['type']
        content_hash = hashlib.md5(memory['content'][:50].encode()).hexdigest()[:8]
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{mem_type}_{timestamp}_{content_hash}.md"
        
        content = f"""---
type: {memory['type']}
confidence: {memory['confidence']}
tags: ["{memory['type']}", "auto-extracted"]
session: {memory['file']}
extracted_at: {memory['extracted_at']}
---

# {memory['type'].replace('-', ' ').title()} - {memory['content'][:80]}...

{memory['content']}

## 来源
- 会话: {memory['file']}
- 类型: {memory['type']}
- 置信度: {memory['confidence']}
"""
        
        (self.memory_dir / filename).write_text(content, encoding='utf-8')
        return filename
    
    def extract_all(self):
        print("🧠 OpenCode Memory Extractor V2")
        print("=" * 40)
        
        if not self.sessions_dir.exists():
            print("⚠️ 会话目录不存在")
            return
        
        sessions = list(self.sessions_dir.glob("*.md"))
        print(f"📚 处理 {len(sessions)} 个会话\n")
        
        total_memories = 0
        for session_file in sessions:
            memories = self.process_session(session_file)
            for memory in memories:
                self.save_memory(memory)
                total_memories += 1
        
        print(f"✅ 提取 {total_memories} 条记忆到 {self.memory_dir}")


if __name__ == "__main__":
    extractor = MemoryExtractor()
    extractor.extract_all()
