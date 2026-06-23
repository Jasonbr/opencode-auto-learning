#!/usr/bin/env python3
"""
OpenCode 技能自动生成器
从重复模式中自动生成技能
"""

import json
import hashlib
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Set, Optional
import re
from difflib import SequenceMatcher

class CommandNormalizer:
    """命令标准化和去重"""
    
    @staticmethod
    def normalize(cmd: str) -> str:
        """标准化命令用于比较和泛化"""
        normalized = cmd
        
        # 1. 替换用户路径
        normalized = re.sub(r'/Users/\w+', '$HOME', normalized)
        normalized = re.sub(r'/home/\w+', '$HOME', normalized)
        
        # 2. 替换时间戳
        normalized = re.sub(r'\d{4}-\d{2}-\d{2}', 'YYYY-MM-DD', normalized)
        normalized = re.sub(r'\d{2}:\d{2}:\d{2}', 'HH:MM:SS', normalized)
        
        # 3. 替换动态 ID (PID、哈希等)
        normalized = re.sub(r'\b[0-9a-f]{8}\b', '<ID>', normalized)
        normalized = re.sub(r'\b\d{4,}\b', '<NUM>', normalized)
        
        # 4. 替换 IP 地址
        normalized = re.sub(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', '<IP>', normalized)
        
        return normalized.strip()
    
    @staticmethod
    def similarity(cmd1: str, cmd2: str) -> float:
        """计算命令相似度 (0-1)"""
        norm1 = CommandNormalizer.normalize(cmd1)
        norm2 = CommandNormalizer.normalize(cmd2)
        return SequenceMatcher(None, norm1, norm2).ratio()
    
    @staticmethod
    def deduplicate(commands: List[str], threshold: float = 0.8) -> List[str]:
        """去重命令列表"""
        if not commands:
            return []
        
        unique_commands = []
        normalized_seen = []
        
        for cmd in commands:
            normalized = CommandNormalizer.normalize(cmd)
            
            # 检查是否与已有命令相似
            is_duplicate = any(
                CommandNormalizer.similarity(normalized, existing) > threshold
                for existing in normalized_seen
            )
            
            if not is_duplicate:
                unique_commands.append(cmd)
                normalized_seen.append(normalized)
        
        return unique_commands
    
    @staticmethod
    def generalize(cmd: str) -> str:
        """泛化命令，用变量替代具体值"""
        generalized = cmd
        
        # 替换为环境变量
        generalized = re.sub(r'/Users/\w+', '$HOME', generalized)
        generalized = re.sub(r'/home/\w+', '$HOME', generalized)
        
        # 替换为占位符
        generalized = re.sub(r'\b[0-9a-f]{8}\b', '<PID>', generalized)
        
        return generalized


class SkillGenerator:
    """技能自动生成器"""
    
    def __init__(self):
        self.memory_dir = Path.home() / ".config/opencode/memory/user"
        self.skills_dir = Path.home() / ".config/opencode/skills/auto-generated"
        self.skills_dir.mkdir(parents=True, exist_ok=True)
        
        # 技能模板
        self.templates = {
            "command": self._command_skill_template,
            "workflow": self._workflow_skill_template,
            "config": self._config_skill_template,
        }
    
    def analyze_memories(self) -> Dict[str, List[Dict]]:
        """分析记忆，发现模式（增强版 - 支持去重）"""
        patterns = {
            "commands": [],
            "workflows": [],
            "configs": [],
        }
        
        # 读取所有记忆文件
        for memory_file in self.memory_dir.glob("*.md"):
            content = memory_file.read_text()
            
            # 提取命令模式
            command_patterns = re.findall(r'```bash\n(.+?)\n```', content, re.DOTALL)
            for cmd in command_patterns:
                if len(cmd.strip()) > 10:
                    patterns["commands"].append({
                        "content": cmd.strip(),
                        "source": memory_file.name,
                        "type": "command"
                    })
            
            # 提取工作流模式
            if "步骤" in content or "流程" in content:
                workflow = self._extract_workflow(content)
                if workflow:
                    patterns["workflows"].append({
                        "content": workflow,
                        "source": memory_file.name,
                        "type": "workflow"
                    })
        
        # 去重命令 (使用 CommandNormalizer)
        if patterns["commands"]:
            raw_commands = [c["content"] for c in patterns["commands"]]
            unique_commands = CommandNormalizer.deduplicate(raw_commands, threshold=0.8)
            
            # 保留去重后的命令
            patterns["commands"] = [
                c for c in patterns["commands"] 
                if c["content"] in unique_commands
            ]
            
            print(f"  🔧 命令去重: {len(raw_commands)} → {len(unique_commands)} (减少 {len(raw_commands) - len(unique_commands)} 个)")
        
        return patterns
    
    def _extract_workflow(self, content: str) -> Optional[str]:
        """提取工作流"""
        # 查找步骤列表
        steps = re.findall(r'\d+\.\s*(.+?)(?:\n|$)', content)
        if len(steps) >= 3:
            return "\n".join(f"{i+1}. {step}" for i, step in enumerate(steps))
        return None
    
    def generate_skill(self, pattern: Dict) -> Optional[Path]:
        """从模式生成技能"""
        pattern_type = pattern.get("type", "command")
        
        if pattern_type not in self.templates:
            return None
        
        # 生成技能名称
        content_hash = hashlib.md5(pattern["content"].encode()).hexdigest()[:8]
        skill_name = f"auto-{pattern_type}-{content_hash}"
        
        # 生成技能文件
        skill_dir = self.skills_dir / skill_name
        skill_dir.mkdir(exist_ok=True)
        
        # 使用模板生成 SKILL.md
        template_fn = self.templates[pattern_type]
        skill_content = template_fn(skill_name, pattern)
        
        skill_file = skill_dir / "SKILL.md"
        with open(skill_file, 'w') as f:
            f.write(skill_content)
        
        # 生成可执行脚本（如果是命令技能）
        if pattern_type == "command":
            script_file = skill_dir / f"{skill_name}.sh"
            script_content = self._generate_script(pattern["content"])
            with open(script_file, 'w') as f:
                f.write(script_content)
            script_file.chmod(0o755)
        
        return skill_file
    
    def _command_skill_template(self, name: str, pattern: Dict) -> str:
        """命令技能模板"""
        return f"""---
name: {name}
auto_generated: true
generated_at: {datetime.now().isoformat()}
source: {pattern.get("source", "unknown")}
---

# Auto-Generated Skill: {name}

## Description

自动生成的命令技能，基于历史使用模式。

## Source Pattern

```bash
{pattern["content"]}
```

## Usage

```bash
{name} [args...]
```

## Notes

- Auto-generated from usage patterns
- Confidence: high
- Review before using in production
"""
    
    def _workflow_skill_template(self, name: str, pattern: Dict) -> str:
        """工作流技能模板"""
        return f"""---
name: {name}
auto_generated: true
generated_at: {datetime.now().isoformat()}
source: {pattern.get("source", "unknown")}
---

# Auto-Generated Workflow: {name}

## Description

自动生成的标准化工作流。

## Steps

{pattern["content"]}

## Usage

Follow the steps above for consistent execution.

## Notes

- Auto-generated from historical patterns
- Review and customize as needed
"""
    
    def _config_skill_template(self, name: str, pattern: Dict) -> str:
        """配置技能模板"""
        return f"""---
name: {name}
auto_generated: true
generated_at: {datetime.now().isoformat()}
---

# Auto-Generated Config: {name}

## Description

常用配置模板。

## Configuration

```
{pattern["content"]}
```

## Notes

- Auto-generated
- Adapt to your specific needs
"""
    
    def _generate_script(self, command: str) -> str:
        """生成可执行脚本"""
        return f"""#!/bin/bash
# Auto-generated command wrapper

{command}
"""
    
    def run_generation(self) -> List[Path]:
        """运行技能生成"""
        patterns = self.analyze_memories()
        generated_skills = []
        
        # 生成命令技能
        for cmd in patterns["commands"][:5]:  # 限制数量
            skill = self.generate_skill(cmd)
            if skill:
                generated_skills.append(skill)
        
        # 生成工作流技能
        for workflow in patterns["workflows"][:3]:
            skill = self.generate_skill(workflow)
            if skill:
                generated_skills.append(skill)
        
        return generated_skills

if __name__ == "__main__":
    generator = SkillGenerator()
    skills = generator.run_generation()
    
    print(f"✅ Generated {len(skills)} skills:")
    for skill in skills:
        print(f"   - {skill.parent.name}")
