#!/usr/bin/env python3
"""
Violation Analyzer - 分析规则违反模式，自动学习
"""

from datetime import datetime
from typing import Dict, List, Any, Optional


class ViolationAnalyzer:
    """分析规则违反模式，自动学习"""
    
    def __init__(self, mem0_client=None, kg_client=None):
        self.mem0 = mem0_client
        self.kg = kg_client
        self.violation_patterns = {}
        
    def analyze_tdd_violation(self, violation: Dict) -> Dict:
        """分析 TDD 违反"""
        pattern = self._identify_tdd_pattern(violation)
        root_cause = self._analyze_root_cause(violation)
        
        analysis = {
            "type": "tdd_violation",
            "pattern": pattern,
            "root_cause": root_cause,
            "recommendation": self._generate_tdd_recommendation(violation),
            "timestamp": datetime.now().isoformat()
        }
        
        # 保存到知识图谱
        if self.kg:
            self.kg.add_node({
                "id": f"violation_{datetime.now().timestamp()}",
                "type": "tdd_violation",
                "pattern": pattern,
                "root_cause": root_cause
            })
        
        return analysis
    
    def _identify_tdd_pattern(self, violation: Dict) -> str:
        """识别 TDD 违反模式"""
        patterns = {
            "implementation_before_test": "写代码前未写测试",
            "skipped_red_phase": "跳过看测试失败阶段",
            "bundle_changes": "一次修改多个功能",
            "no_regression_check": "未运行完整测试套件"
        }
        
        vtype = violation.get("type", "unknown")
        return patterns.get(vtype, "unknown")
    
    def _analyze_root_cause(self, violation: Dict) -> str:
        """分析根本原因"""
        causes = {
            "time_pressure": "时间压力导致跳过测试",
            "unfamiliarity": "不熟悉 TDD 流程",
            "overconfidence": "过度自信认为不需要测试",
            "complexity": "代码太复杂难以测试"
        }
        
        return causes.get(
            violation.get("cause", "unknown"),
            "未知原因"
        )
    
    def _generate_tdd_recommendation(self, violation: Dict) -> str:
        """生成 TDD 改进建议"""
        return """
## TDD 最佳实践

### 正确做法:
1. 先写测试 - 确保测试失败
2. 写最小代码 - 让测试通过
3. 运行完整测试 - 确保无回归
4. 重构代码 - 保持测试绿色

### 常见陷阱:
- ❌ 写实现前不写测试
- ❌ 跳过看测试失败阶段
- ❌ 一次修改多个功能
- ❌ 提交前不运行完整测试

### 参考案例:
查看知识图谱中的 tdd_success 节点
"""


if __name__ == "__main__":
    print("ViolationAnalyzer loaded successfully")
