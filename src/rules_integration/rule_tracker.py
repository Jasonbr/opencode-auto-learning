#!/usr/bin/env python3
"""
Rule Tracker - 跟踪规则执行情况并记录到学习系统
"""

from datetime import datetime
from typing import Dict, List, Optional, Any
import json
import hashlib


class RuleTracker:
    """跟踪防套娃规则执行情况"""
    
    def __init__(self, mem0_client=None, kg_client=None):
        self.mem0 = mem0_client
        self.kg = kg_client
        self.execution_history = []
        
    def track_tdd_execution(self, context: Dict) -> Dict:
        """记录 TDD 执行情况"""
        memory = {
            "type": "pattern",
            "category": "tdd_compliance",
            "content": {
                "rule": "tdd-enforcement",
                "project": context.get("project", "unknown"),
                "file": context.get("file", "unknown"),
                "compliance": {
                    "test_written_first": context.get("test_written_first", False),
                    "test_failed_first": context.get("test_failed_first", False),
                    "implementation_minimal": context.get("implementation_minimal", False),
                    "all_tests_pass": context.get("all_tests_pass", False)
                },
                "regressions": context.get("regressions", 0),
                "timestamp": datetime.now().isoformat(),
                "success": self._calculate_tdd_success(context)
            },
            "tags": ["tdd", "testing", "regression"]
        }
        
        if self.mem0:
            self.mem0.save(memory)
            
        if self.kg:
            self._update_kg_with_tdd_pattern(memory)
            
        self.execution_history.append(memory)
        return memory
    
    def track_precommit_checks(self, results: Dict) -> Dict:
        """记录预提交检查结果"""
        memory = {
            "type": "pattern",
            "category": "precommit_compliance",
            "content": {
                "rule": "pre-commit-verification",
                "security": {
                    "secrets_found": results.get("secrets_found", 0),
                    "tests_passed": results.get("tests_passed", False),
                    "lint_clean": results.get("lint_clean", False),
                    "new_failures": results.get("new_failures", 0)
                },
                "timestamp": datetime.now().isoformat(),
                "passed": self._calculate_precommit_success(results)
            },
            "tags": ["security", "quality", "regression"]
        }
        
        if self.mem0:
            self.mem0.save(memory)
            
        self.execution_history.append(memory)
        return memory
    
    def track_three_strikes(self, failure: Dict) -> Optional[Dict]:
        """记录 3 次失败法则触发"""
        attempt = failure.get("attempt", 0)
        
        if attempt < 3:
            return None
            
        memory = {
            "type": "learning",
            "category": "architecture_insight",
            "content": {
                "rule": "three-strikes",
                "attempts": attempt,
                "pattern": "architectural_problem_detected",
                "project": failure.get("project", "unknown"),
                "error": failure.get("error_message", ""),
                "recommendation": "Consider refactoring architecture",
                "severity": "high"
            },
            "tags": ["architecture", "refactoring", "design"]
        }
        
        if self.mem0:
            self.mem0.save(memory)
            
        insight = self._generate_architecture_insight(failure)
        self.execution_history.append(memory)
        
        return insight
    
    def _calculate_tdd_success(self, context: Dict) -> bool:
        """计算 TDD 是否成功"""
        compliance = context.get("compliance", {})
        return all([
            compliance.get("test_written_first", False),
            compliance.get("test_failed_first", False),
            compliance.get("implementation_minimal", False),
            compliance.get("all_tests_pass", False)
        ])
    
    def _calculate_precommit_success(self, results: Dict) -> bool:
        """计算预提交检查是否通过"""
        return (
            results.get("secrets_found", 0) == 0 and
            results.get("tests_passed", False) and
            results.get("lint_clean", False) and
            results.get("new_failures", 0) == 0
        )
    
    def _update_kg_with_tdd_pattern(self, memory: Dict):
        """更新知识图谱"""
        if not self.kg:
            return
            
        compliance = memory.get("content", {}).get("compliance", {})
        project = memory.get("content", {}).get("project", "unknown")
        file_path = memory.get("content", {}).get("file", "unknown")
        
        if all(compliance.values()):
            node = {
                "id": f"tdd_success_{hashlib.md5(f'{project}:{file_path}'.encode()).hexdigest()[:8]}",
                "type": "tdd_success",
                "project": project,
                "file": file_path
            }
        else:
            violations = [k for k, v in compliance.items() if not v]
            node = {
                "id": f"tdd_violation_{hashlib.md5(f'{project}:{file_path}'.encode()).hexdigest()[:8]}",
                "type": "tdd_violation",
                "violations": violations,
                "project": project
            }
        
        self.kg.add_node(node)
    
    def _generate_architecture_insight(self, failure: Dict) -> Dict:
        """生成架构洞察"""
        fix_desc = failure.get("fix_description", "")
        
        patterns = []
        if "broke" in fix_desc.lower():
            patterns.append("fix_breaks_other")
        if "circular" in fix_desc.lower():
            patterns.append("circular_dependency")
        if "state" in fix_desc.lower():
            patterns.append("shared_state")
            
        return {
            "title": "架构问题检测",
            "problem": failure.get("error_message", "Unknown"),
            "attempts": failure.get("attempt", 0),
            "patterns_detected": patterns,
            "indicators": [
                "多次修复失败",
                "修复引入新问题",
                "症状在不同模块间移动"
            ],
            "recommendations": self._generate_recommendations(patterns)
        }
    
    def _generate_recommendations(self, patterns: List) -> List:
        """根据模式生成建议"""
        recommendations = []
        
        if "circular_dependency" in patterns:
            recommendations.append("1. 引入接口层，打破循环依赖")
            recommendations.append("2. 使用依赖注入模式")
            
        if "shared_state" in patterns:
            recommendations.append("3. 隔离状态，使用纯函数")
            
        return recommendations if recommendations else ["1. 进行代码审查"]
    
    def get_execution_stats(self) -> Dict:
        """获取执行统计"""
        if not self.execution_history:
            return {"total": 0, "success_rate": 0}
            
        total = len(self.execution_history)
        successful = sum(1 for h in self.execution_history 
                         if h.get("content", {}).get("success", False))
        
        return {
            "total": total,
            "successful": successful,
            "success_rate": successful / total if total > 0 else 0
        }


if __name__ == "__main__":
    print("RuleTracker loaded successfully")
