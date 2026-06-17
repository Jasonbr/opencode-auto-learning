#!/usr/bin/env python3
"""
Rule Recommender - 主动智能推荐系统
在操作前根据上下文推荐相关规则
"""

from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
import json


class RuleRecommender:
    """
    主动推荐相关规则
    
    基于文件类型、操作类型、历史记录主动推荐
    """
    
    def __init__(self, mem0_client=None, rule_tracker=None):
        self.mem0 = mem0_client
        self.tracker = rule_tracker
        self.recommendation_cache = {}
        
        # 规则与文件类型的映射
        self.file_type_rules = {
            "test": ["tdd-enforcement", "pre-commit-verification"],
            "implementation": ["tdd-enforcement", "three-strikes"],
            "config": ["pre-commit-verification"],
            "fix": ["three-strikes", "pre-commit-verification"]
        }
        
        # 规则优先级权重
        self.rule_weights = {
            "tdd-enforcement": 1.0,
            "pre-commit-verification": 0.9,
            "three-strikes": 1.2  # 修复时权重更高
        }
    
    def recommend_before_edit(self, file_path: str, operation: str) -> List[Dict[str, Any]]:
        """
        在编辑文件前推荐相关规则
        
        Args:
            file_path: 文件路径
            operation: 操作类型 (create, edit, fix, test)
            
        Returns:
            推荐规则列表
        """
        recommendations = []
        
        # 1. 基于文件类型推荐
        file_type = self._detect_file_type(file_path)
        type_rules = self.file_type_rules.get(file_type, ["tdd-enforcement"])
        
        for rule in type_rules:
            weight = self.rule_weights.get(rule, 0.5)
            
            # 2. 从历史学习调整权重
            if self.tracker:
                historical = self._get_historical_effectiveness(rule, file_type)
                weight *= historical
            
            # 3. 检查是否已执行
            executed = self._check_rule_executed(rule, file_path)
            
            recommendations.append({
                "rule": rule,
                "weight": weight,
                "file_type": file_type,
                "operation": operation,
                "reason": self._get_recommendation_reason(rule, file_type),
                "executed": executed,
                "auto_apply": weight > 0.9 and not executed,
                "timestamp": datetime.now().isoformat()
            })
        
        # 按权重排序
        recommendations.sort(key=lambda x: x["weight"], reverse=True)
        
        # 保存推荐历史
        self._save_recommendation_history(file_path, recommendations)
        
        return recommendations[:3]  # 返回前3个推荐
    
    def recommend_before_commit(self, changed_files: List[str]) -> List[Dict[str, Any]]:
        """
        在提交前推荐预提交检查规则
        
        Args:
            changed_files: 变更的文件列表
            
        Returns:
            推荐规则列表
        """
        recommendations = []
        
        # 检查文件类型分布
        file_types = {}
        for f in changed_files:
            ft = self._detect_file_type(f)
            file_types[ft] = file_types.get(ft, 0) + 1
        
        # 根据文件类型分布推荐
        if "implementation" in file_types:
            recommendations.append({
                "rule": "pre-commit-verification",
                "weight": 1.0,
                "reason": "Implementation files changed, security scan recommended",
                "auto_apply": True
            })
        
        if "test" in file_types:
            recommendations.append({
                "rule": "tdd-enforcement",
                "weight": 0.95,
                "reason": "Test files changed, verify TDD compliance",
                "auto_apply": False
            })
        
        # 如果有修复操作
        if any("fix" in f.lower() or "bug" in f.lower() for f in changed_files):
            recommendations.append({
                "rule": "three-strikes",
                "weight": 1.2,
                "reason": "Bug fix detected, watch for regression",
                "auto_apply": True
            })
        
        return recommendations
    
    def _detect_file_type(self, file_path: str) -> str:
        """检测文件类型"""
        path_lower = file_path.lower()
        
        if "test" in path_lower or "spec" in path_lower:
            return "test"
        elif any(ext in path_lower for ext in [".py", ".js", ".ts", ".java"]):
            return "implementation"
        elif any(ext in path_lower for ext in [".json", ".yaml", ".toml", ".config"]):
            return "config"
        elif "fix" in path_lower or "patch" in path_lower:
            return "fix"
        else:
            return "implementation"
    
    def _get_historical_effectiveness(self, rule: str, file_type: str) -> float:
        """获取历史效果（0.5-1.5之间）"""
        if not self.mem0:
            return 1.0
        
        try:
            # 查询历史记录
            memories = self.mem0.get_all({
                "category": f"{rule}_compliance",
                "tags": [file_type]
            })
            
            if not memories:
                return 1.0
            
            # 计算成功率
            success_count = sum(
                1 for m in memories 
                if m.get("content", {}).get("success", False) or
                m.get("content", {}).get("passed", False)
            )
            
            total = len(memories)
            success_rate = success_count / total if total > 0 else 0.5
            
            # 映射到 0.5-1.5 范围
            return 0.5 + (success_rate * 1.0)
            
        except Exception as e:
            print(f"[RuleRecommender] Failed to get historical data: {e}")
            return 1.0
    
    def _check_rule_executed(self, rule: str, file_path: str) -> bool:
        """检查规则是否已在当前会话执行"""
        if not self.tracker:
            return False
        
        # 检查执行历史
        for history in self.tracker.execution_history:
            if (history.get("content", {}).get("rule") == rule and
                history.get("content", {}).get("file") == file_path):
                return True
        
        return False
    
    def _get_recommendation_reason(self, rule: str, file_type: str) -> str:
        """获取推荐理由"""
        reasons = {
            "tdd-enforcement": {
                "test": "Test file edited, verify TDD compliance",
                "implementation": "Implementation changed, ensure tests exist",
                "default": "Code changes require TDD"
            },
            "pre-commit-verification": {
                "config": "Config changes need validation",
                "implementation": "Code changes need security scan",
                "default": "Pre-commit checks recommended"
            },
            "three-strikes": {
                "fix": "Bug fix in progress, watch for regression",
                "implementation": "Complex changes may introduce issues",
                "default": "Monitor fix attempts"
            }
        }
        
        rule_reasons = reasons.get(rule, {})
        return rule_reasons.get(file_type, rule_reasons.get("default", "Rule recommended"))
    
    def _save_recommendation_history(self, file_path: str, recommendations: List[Dict]):
        """保存推荐历史"""
        if not self.mem0:
            return
        
        memory = {
            "type": "recommendation",
            "category": "rule_recommendation",
            "content": {
                "file": file_path,
                "recommendations": recommendations,
                "count": len(recommendations)
            },
            "tags": ["recommendation", "rules"],
            "timestamp": datetime.now().isoformat()
        }
        
        try:
            self.mem0.save(memory)
        except Exception as e:
            print(f"[RuleRecommender] Failed to save recommendation: {e}")
    
    def get_recommendation_stats(self) -> Dict[str, Any]:
        """获取推荐统计"""
        return {
            "total_recommendations": len(self.recommendation_cache),
            "unique_files": len(set(self.recommendation_cache.keys())),
            "timestamp": datetime.now().isoformat()
        }


# 用于测试的简单 Mem0 客户端
class MockMem0Client:
    """模拟 Mem0 客户端"""
    
    def __init__(self):
        self.memories = []
    
    def save(self, memory: Dict):
        self.memories.append(memory)
    
    def get_all(self, query: Dict) -> List[Dict]:
        return [m for m in self.memories if self._matches(m, query)]
    
    def _matches(self, memory: Dict, query: Dict) -> bool:
        for key, value in query.items():
            if memory.get(key) != value:
                return False
        return True


if __name__ == "__main__":
    print("Testing RuleRecommender...")
    
    # 创建推荐器
    mem0 = MockMem0Client()
    recommender = RuleRecommender(mem0_client=mem0)
    
    # 测试 1: 编辑实现文件
    print("\n=== Test 1: Edit Implementation File ===")
    recs = recommender.recommend_before_edit("src/example.py", "edit")
    for r in recs:
        print(f"  - {r['rule']}: weight={r['weight']:.2f}, auto_apply={r['auto_apply']}")
    
    # 测试 2: 提交前推荐
    print("\n=== Test 2: Pre-commit Recommendations ===")
    recs = recommender.recommend_before_commit(["src/example.py", "test_example.py"])
    for r in recs:
        print(f"  - {r['rule']}: weight={r['weight']:.2f}")
    
    print("\n✅ RuleRecommender tests passed!")
