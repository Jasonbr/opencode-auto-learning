#!/usr/bin/env python3
"""
Rule Based Skill Generator - 从防套娃模式生成技能
从成功案例自动提取最佳实践
"""

from datetime import datetime
from typing import Dict, List, Any, Optional
import json
import hashlib


class RuleBasedSkillGenerator:
    """
    从防套娃规则执行生成可复用技能
    """
    
    def __init__(self, mem0_client=None, kg_client=None):
        self.mem0 = mem0_client
        self.kg = kg_client
        self.skill_templates = self._load_skill_templates()
    
    def _load_skill_templates(self) -> Dict[str, Any]:
        """加载技能模板"""
        return {
            "tdd": {
                "name": "tdd-{pattern}",
                "description": "TDD pattern for {context}",
                "steps": [
                    "Write failing test",
                    "Run test - confirm RED",
                    "Write minimal code",
                    "Run test - confirm GREEN",
                    "Refactor if needed"
                ]
            },
            "precommit": {
                "name": "precommit-{pattern}",
                "description": "Pre-commit verification pattern",
                "steps": [
                    "Scan for secrets",
                    "Run tests",
                    "Check lint",
                    "Verify no regressions"
                ]
            },
            "architecture": {
                "name": "architecture-{pattern}",
                "description": "Architecture refactoring pattern",
                "steps": [
                    "Identify dependencies",
                    "Break circular references",
                    "Introduce interfaces",
                    "Update tests"
                ]
            }
        }
    
    def generate_from_successes(self, rule: str, min_samples: int = 3) -> Optional[Dict[str, Any]]:
        """
        从成功案例生成技能
        
        Args:
            rule: 规则名称
            min_samples: 最小样本数
            
        Returns:
            生成的技能
        """
        if not self.mem0:
            return None
        
        try:
            # 获取成功案例
            successes = self._get_successful_executions(rule, min_samples)
            
            if len(successes) < min_samples:
                return None
            
            # 提取模式
            pattern = self._extract_pattern(successes)
            
            # 生成技能
            skill = self._create_skill(rule, pattern, successes)
            
            # 保存到知识图谱
            if self.kg:
                self._save_skill_to_kg(skill)
            
            return skill
            
        except Exception as e:
            print(f"[SkillGenerator] Error generating skill: {e}")
            return None
    
    def _get_successful_executions(self, rule: str, min_samples: int) -> List[Dict]:
        """获取成功执行记录"""
        category = f"{rule.replace('-', '_')}_compliance"
        
        memories = self.mem0.get_all({
            "category": category
        })
        
        # 过滤成功案例
        successes = [
            m for m in memories
            if m.get("content", {}).get("success", False) or
            m.get("content", {}).get("passed", False)
        ]
        
        return successes[:min_samples * 2]  # 取更多样本用于分析
    
    def _extract_pattern(self, successes: List[Dict]) -> Dict[str, Any]:
        """从成功案例中提取模式"""
        # 统计共性
        contexts = {}
        
        for s in successes:
            content = s.get("content", {})
            file_type = self._detect_file_type(content.get("file", ""))
            
            contexts[file_type] = contexts.get(file_type, 0) + 1
        
        # 找出最常见的上下文
        most_common = max(contexts.items(), key=lambda x: x[1])
        
        return {
            "context": most_common[0],
            "frequency": most_common[1],
            "total_samples": len(successes)
        }
    
    def _create_skill(self, rule: str, pattern: Dict, successes: List[Dict]) -> Dict[str, Any]:
        """创建技能"""
        # 选择模板
        if "tdd" in rule:
            template = self.skill_templates["tdd"]
        elif "precommit" in rule:
            template = self.skill_templates["precommit"]
        else:
            template = self.skill_templates["architecture"]
        
        # 生成技能 ID
        skill_id = hashlib.md5(
            f"{rule}:{pattern['context']}:{datetime.now().timestamp()}".encode()
        ).hexdigest()[:8]
        
        skill = {
            "id": f"skill-{skill_id}",
            "name": template["name"].format(pattern=pattern["context"]),
            "description": template["description"].format(context=pattern["context"]),
            "source_rule": rule,
            "pattern": pattern,
            "steps": template["steps"],
            "success_rate": len(successes) / (len(successes) + 5),  # 保守估计
            "generated_from": len(successes),
            "timestamp": datetime.now().isoformat(),
            "type": "auto_generated"
        }
        
        return skill
    
    def _save_skill_to_kg(self, skill: Dict[str, Any]):
        """保存技能到知识图谱"""
        if not self.kg:
            return
        
        node = {
            "id": skill["id"],
            "type": "skill",
            "name": skill["name"],
            "description": skill["description"],
            "success_rate": skill["success_rate"],
            "source_rule": skill["source_rule"]
        }
        
        self.kg.add_node(node)
    
    def _detect_file_type(self, file_path: str) -> str:
        """检测文件类型"""
        path_lower = file_path.lower()
        
        if "test" in path_lower:
            return "test"
        elif any(ext in path_lower for ext in [".py", ".js", ".ts"]):
            return "code"
        elif "config" in path_lower:
            return "config"
        else:
            return "general"
    
    def generate_all_skills(self) -> List[Dict[str, Any]]:
        """生成所有规则的技能"""
        rules = ["tdd-enforcement", "pre-commit-verification", "three-strikes"]
        skills = []
        
        for rule in rules:
            skill = self.generate_from_successes(rule)
            if skill:
                skills.append(skill)
        
        return skills


if __name__ == "__main__":
    print("Testing RuleBasedSkillGenerator...")
    
    generator = RuleBasedSkillGenerator()
    
    print("\n✅ RuleBasedSkillGenerator loaded successfully")
    print("(Note: Requires Mem0 client with data to generate actual skills)")
