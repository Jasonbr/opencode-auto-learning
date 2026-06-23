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
        """分析记忆，发现模式"""
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
