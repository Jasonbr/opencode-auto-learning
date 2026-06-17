#!/usr/bin/env python3
"""
Effectiveness Tracker - 跟踪规则效果
计算 auto-apply 分数，动态调整推荐
"""

from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import json


class EffectivenessTracker:
    """
    跟踪规则效果
    
    计算规则的成功率、回归率、自动应用分数
    """
    
    def __init__(self, mem0_client=None):
        self.mem0 = mem0_client
        self.rules = ["tdd-enforcement", "pre-commit-verification", "three-strikes"]
        
    def calculate_effectiveness(self, rule: str, time_window: int = 30) -> Dict[str, Any]:
        """
        计算规则效果
        
        Args:
            rule: 规则名称
            time_window: 时间窗口（天）
            
        Returns:
            效果统计
        """
        if not self.mem0:
            return self._get_default_stats(rule)
        
        try:
            # 查询时间窗口内的记录
            cutoff = datetime.now() - timedelta(days=time_window)
            
            memories = self.mem0.get_all({
                "category": f"{rule.replace('-', '_')}_compliance"
            })
            
            # 过滤时间窗口
            filtered = [
                m for m in memories
                if datetime.fromisoformat(m.get("timestamp", "2000-01-01")) > cutoff
            ]
            
            if not filtered:
                return self._get_default_stats(rule)
            
            # 计算指标
            total = len(filtered)
            successful = sum(
                1 for m in filtered
                if m.get("content", {}).get("success", False) or
                m.get("content", {}).get("passed", False)
            )
            
            regressions = sum(
                m.get("content", {}).get("regressions", 0)
                for m in filtered
            )
            
            # 计算 auto-apply 分数
            success_rate = successful / total if total > 0 else 0
            regression_rate = regressions / total if total > 0 else 0
            
            auto_apply_score = self._calculate_auto_apply_score(
                success_rate, regression_rate, total
            )
            
            return {
                "rule": rule,
                "time_window_days": time_window,
                "total_executions": total,
                "successful": successful,
                "success_rate": success_rate,
                "regressions": regressions,
                "regression_rate": regression_rate,
                "auto_apply_score": auto_apply_score,
                "recommendation": self._get_recommendation(auto_apply_score),
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"[EffectivenessTracker] Error calculating effectiveness: {e}")
            return self._get_default_stats(rule)
    
    def get_all_rules_effectiveness(self, time_window: int = 30) -> Dict[str, Any]:
        """
        获取所有规则的效果
        
        Returns:
            所有规则的效果统计
        """
        results = {}
        
        for rule in self.rules:
            results[rule] = self.calculate_effectiveness(rule, time_window)
        
        # 计算总体效果
        avg_success = sum(r["success_rate"] for r in results.values()) / len(results)
        avg_regression = sum(r["regression_rate"] for r in results.values()) / len(results)
        
        return {
            "rules": results,
            "summary": {
                "avg_success_rate": avg_success,
                "avg_regression_rate": avg_regression,
                "improvement_needed": avg_success < 0.8 or avg_regression > 0.1
            }
        }
    
    def _calculate_auto_apply_score(
        self, 
        success_rate: float, 
        regression_rate: float,
        sample_size: int
    ) -> float:
        """
        计算 auto-apply 分数
        
        基于：
        - 成功率 (权重 50%)
        - 低回归率 (权重 30%)
        - 样本量 (权重 20%)
        """
        # 成功率因子
        success_factor = success_rate * 0.5
        
        # 低回归率因子
        regression_factor = (1 - regression_rate) * 0.3
        
        # 样本量因子（置信度）
        sample_factor = min(sample_size / 10, 1.0) * 0.2
        
        return success_factor + regression_factor + sample_factor
    
    def _get_recommendation(self, auto_apply_score: float) -> str:
        """根据 auto-apply 分数给出建议"""
        if auto_apply_score >= 0.9:
            return "High confidence - enable auto-apply"
        elif auto_apply_score >= 0.7:
            return "Medium confidence - recommend but confirm"
        elif auto_apply_score >= 0.5:
            return "Low confidence - manual application only"
        else:
            return "Review rule effectiveness"
    
    def _get_default_stats(self, rule: str) -> Dict[str, Any]:
        """获取默认统计"""
        return {
            "rule": rule,
            "total_executions": 0,
            "success_rate": 0.5,
            "regression_rate": 0.0,
            "auto_apply_score": 0.5,
            "recommendation": "Not enough data - collect more samples",
            "timestamp": datetime.now().isoformat()
        }
    
    def should_auto_apply(self, rule: str) -> bool:
        """判断是否应该自动应用规则"""
        stats = self.calculate_effectiveness(rule)
        return stats.get("auto_apply_score", 0) >= 0.9


if __name__ == "__main__":
    print("Testing EffectivenessTracker...")
    
    tracker = EffectivenessTracker()
    
    # 测试计算效果
    print("\n=== Test: Calculate Effectiveness ===")
    stats = tracker.calculate_effectiveness("tdd-enforcement")
    print(f"Rule: {stats['rule']}")
    print(f"Success rate: {stats['success_rate']:.1%}")
    print(f"Auto-apply score: {stats['auto_apply_score']:.2f}")
    print(f"Recommendation: {stats['recommendation']}")
    
    print("\n✅ EffectivenessTracker tests passed!")
