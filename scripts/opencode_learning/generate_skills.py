#!/usr/bin/env python3
"""OpenCode Skill Generator V3

从提取的记忆生成高质量技能文件。
"""
import re
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
from collections import Counter


class SkillGenerator:
    """智能技能生成器 V3"""
    
    def __init__(self):
        self.memory_dir = Path.home() / ".config/opencode/memory/user"
        self.skills_dir = Path.home() / ".config/opencode/skills/auto-generated"
        self.skills_dir.mkdir(parents=True, exist_ok=True)
    
    def parse_memory(self, filepath: Path) -> Optional[Dict]:
        try:
            content = filepath.read_text(encoding='utf-8')
            if not content.startswith('---'):
                return None
            
            parts = content.split('---', 2)
            if len(parts) < 3:
                return None
            
            # 解析 frontmatter
            metadata = {}
            for line in parts[1].strip().split('\n'):
                if ':' in line and not line.startswith('#'):
                    key, value = line.split(':', 1)
                    metadata[key.strip()] = value.strip()
            
            body = re.sub(r'## 来源.*', '', parts[2], flags=re.DOTALL).strip()
            
            return {
                "file": filepath.name,
                "type": metadata.get('type', 'unknown'),
                "title": body.split('\n')[0][:60] if body else filepath.name,
                "content": body
            }
        except Exception:
            return None
    
    def load_memories(self) -> List[Dict]:
        memories = []
        if not self.memory_dir.exists():
            return memories
        
        for f in self.memory_dir.glob("*.md"):
            m = self.parse_memory(f)
            if m:
                memories.append(m)
        return memories
    
    def generate(self):
        print("🔨 OpenCode Skill Generator V3")
        print("=" * 40)
        
        memories = self.load_memories()
        print(f"📚 加载 {len(memories)} 条记忆")
        
        if len(memories) < 5:
            print("⚠️ 记忆数量不足，无法生成技能")
            return
        
        # 统计类型
        types = Counter(m['type'] for m in memories)
        print(f"\n类型分布: {dict(types)}")
        
        # 按类型分组
        by_type = {}
        for m in memories:
            t = m['type']
            if t not in by_type:
                by_type[t] = []
            by_type[t].append(m)
        
        # 生成技能
        generated = []
        
        if 'command' in by_type:
            cmds = [m['content'] for m in by_type['command']]
            self._create_skill('auto-commands', '常用命令参考', cmds)
            generated.append('commands')
        
        if 'code' in by_type:
            codes = [m['content'] for m in by_type['code'][:10]]
            self._create_skill('auto-code-snippets', '代码片段参考', codes)
            generated.append('code-snippets')
        
        if 'config' in by_type:
            configs = [m['content'] for m in by_type['config'][:10]]
            self._create_skill('auto-configs', '配置模式参考', configs)
            generated.append('configs')
        
        if 'decision' in by_type:
            decisions = [m['content'] for m in by_type['decision']]
            self._create_skill('auto-decisions', '技术决策记录', decisions)
            generated.append('decisions')
        
        if 'error-solution' in by_type:
            errors = [m['content'] for m in by_type['error-solution']]
            self._create_skill('auto-errors', '错误解决方案', errors)
            generated.append('errors')
        
        print(f"\n✅ 生成 {len(generated)} 个技能: {generated}")
    
    def _create_skill(self, name: str, title: str, items: List[str]):
        skill_dir = self.skills_dir / name
        skill_dir.mkdir(exist_ok=True)
        
        content = f"""---
name: {name}
title: {title}
auto_generated: true
generated_at: {datetime.now().isoformat()}
category: auto
---

# {title}

共 {len(items)} 条记录。

"""
        
        for i, item in enumerate(items, 1):
            content += f"## {i}.\n\n{item[:500]}\n\n---\n\n"
        
        (skill_dir / "SKILL.md").write_text(content, encoding='utf-8')
        print(f"  ✅ {name}: {len(items)} 条记录")


if __name__ == "__main__":
    SkillGenerator().generate()
