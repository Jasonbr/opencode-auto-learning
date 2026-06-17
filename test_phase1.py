#!/usr/bin/env python3
"""
Phase 1 集成测试
"""

import sys
sys.path.insert(0, '~/opencode-auto-learning/src')

from rules_integration.rule_tracker import RuleTracker
from rules_integration.violation_analyzer import ViolationAnalyzer

def test_rule_tracker():
    """测试 RuleTracker"""
    print("Testing RuleTracker...")
    
    tracker = RuleTracker()
    
    # 测试 TDD 跟踪
    result = tracker.track_tdd_execution({
        "project": "test-project",
        "file": "test.py",
        "test_written_first": True,
        "test_failed_first": True,
        "implementation_minimal": True,
        "all_tests_pass": True,
        "regressions": 0
    })
    
    assert result["content"]["success"] == True
    print("✅ TDD tracking test passed")
    
    # 测试预提交跟踪
    result = tracker.track_precommit_checks({
        "secrets_found": 0,
        "tests_passed": True,
        "lint_clean": True,
        "new_failures": 0
    })
    
    assert result["content"]["passed"] == True
    print("✅ Pre-commit tracking test passed")
    
    # 测试统计
    stats = tracker.get_execution_stats()
    assert stats["total"] == 2
    print(f"✅ Statistics: {stats}")
    
    print("\n✅ RuleTracker tests passed!")

def test_violation_analyzer():
    """测试 ViolationAnalyzer"""
    print("\nTesting ViolationAnalyzer...")
    
    analyzer = ViolationAnalyzer()
    
    result = analyzer.analyze_tdd_violation({
        "type": "implementation_before_test",
        "cause": "time_pressure"
    })
    
    assert result["pattern"] == "写代码前未写测试"
    assert result["root_cause"] == "时间压力导致跳过测试"
    print("✅ Violation analysis test passed")
    
    print("\n✅ ViolationAnalyzer tests passed!")

if __name__ == "__main__":
    print("=" * 60)
    print("Running Phase 1 Integration Tests")
    print("=" * 60)
    
    test_rule_tracker()
    test_violation_analyzer()
    
    print("\n" + "=" * 60)
    print("🎉 All tests passed!")
    print("=" * 60)
