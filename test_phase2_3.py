#!/usr/bin/env python3
"""
Phase 2 & 3 Integration Tests
测试主动推荐和智能技能生成
"""

import sys
sys.path.insert(0, '~/opencode-auto-learning/src')

from rules_integration import (
    RuleRecommender,
    EffectivenessTracker,
    RuleBasedSkillGenerator,
    ArchitectureSolutionGenerator
)


class MockMem0Client:
    """模拟 Mem0 客户端"""
    def __init__(self):
        self.memories = []
    
    def save(self, memory):
        self.memories.append(memory)
        print(f"  [MockMem0] Saved: {memory.get('type')} - {memory.get('category')}")
    
    def get_all(self, query):
        return [m for m in self.memories if self._matches(m, query)]
    
    def _matches(self, memory, query):
        for key, value in query.items():
            if memory.get(key) != value:
                return False
        return True


def test_rule_recommender():
    """测试 RuleRecommender"""
    print("\n" + "="*60)
    print("Testing RuleRecommender")
    print("="*60)
    
    mem0 = MockMem0Client()
    recommender = RuleRecommender(mem0_client=mem0)
    
    # 测试 1: 编辑文件前推荐
    print("\nTest 1: Recommend before edit")
    recs = recommender.recommend_before_edit("src/example.py", "edit")
    print(f"  Recommendations: {len(recs)}")
    for r in recs:
        print(f"    - {r['rule']}: weight={r['weight']:.2f}, auto_apply={r['auto_apply']}")
    assert len(recs) > 0
    print("  ✅ Test 1 passed")
    
    # 测试 2: 提交前推荐
    print("\nTest 2: Recommend before commit")
    recs = recommender.recommend_before_commit(["src/a.py", "test_b.py"])
    print(f"  Recommendations: {len(recs)}")
    for r in recs:
        print(f"    - {r['rule']}: {r['reason'][:50]}...")
    assert len(recs) > 0
    print("  ✅ Test 2 passed")
    
    print("\n✅ RuleRecommender tests passed!")


def test_effectiveness_tracker():
    """测试 EffectivenessTracker"""
    print("\n" + "="*60)
    print("Testing EffectivenessTracker")
    print("="*60)
    
    tracker = EffectivenessTracker()
    
    # 测试 1: 计算单规则效果
    print("\nTest 1: Calculate single rule effectiveness")
    stats = tracker.calculate_effectiveness("tdd-enforcement")
    print(f"  Rule: {stats['rule']}")
    print(f"  Success rate: {stats['success_rate']:.1%}")
    print(f"  Auto-apply score: {stats['auto_apply_score']:.2f}")
    print(f"  Recommendation: {stats['recommendation']}")
    assert stats['rule'] == 'tdd-enforcement'
    print("  ✅ Test 1 passed")
    
    # 测试 2: 计算所有规则效果
    print("\nTest 2: Calculate all rules effectiveness")
    results = tracker.get_all_rules_effectiveness()
    print(f"  Rules tracked: {len(results['rules'])}")
    print(f"  Avg success rate: {results['summary']['avg_success_rate']:.1%}")
    print(f"  Improvement needed: {results['summary']['improvement_needed']}")
    assert len(results['rules']) > 0
    print("  ✅ Test 2 passed")
    
    print("\n✅ EffectivenessTracker tests passed!")


def test_skill_generator():
    """测试 RuleBasedSkillGenerator"""
    print("\n" + "="*60)
    print("Testing RuleBasedSkillGenerator")
    print("="*60)
    
    mem0 = MockMem0Client()
    generator = RuleBasedSkillGenerator(mem0_client=mem0)
    
    # 测试 1: 加载
    print("\nTest 1: Module loaded")
    print(f"  Templates: {len(generator.skill_templates)}")
    assert len(generator.skill_templates) > 0
    print("  ✅ Test 1 passed")
    
    # 测试 2: 技能生成（需要数据）
    print("\nTest 2: Generate skills (requires data)")
    skills = generator.generate_all_skills()
    print(f"  Skills generated: {len(skills)}")
    print("  (Note: Returns empty without Mem0 data)")
    print("  ✅ Test 2 passed")
    
    print("\n✅ RuleBasedSkillGenerator tests passed!")


def test_architecture_generator():
    """测试 ArchitectureSolutionGenerator"""
    print("\n" + "="*60)
    print("Testing ArchitectureSolutionGenerator")
    print("="*60)
    
    generator = ArchitectureSolutionGenerator()
    
    # 测试 1: 生成循环依赖解决方案
    print("\nTest 1: Generate circular dependency solution")
    solution = generator.generate_solution("circular_dependency", {
        "attempts": 3,
        "error": "Circular import",
        "files": ["a.py", "b.py"]
    })
    print(f"  Title: {solution['title']}")
    print(f"  Steps: {len(solution['steps'])}")
    print(f"  Estimated time: {solution['estimated_time']}")
    print(f"  Risk level: {solution['risk_level']}")
    assert solution['problem_type'] == 'circular_dependency'
    print("  ✅ Test 1 passed")
    
    # 测试 2: 从 3 次失败生成
    print("\nTest 2: Generate from three strikes")
    solution = generator.generate_from_three_strikes({
        "attempt": 3,
        "fix_description": "Fixed A, broke B; Fixed B broke C - circular dependency detected",
        "error_message": "ImportError: cannot import name"
    })
    print(f"  Detected type: {solution['problem_type']}")
    print(f"  Solution: {solution['title']}")
    assert solution is not None
    print("  ✅ Test 2 passed")
    
    # 测试 3: 检测问题类型
    print("\nTest 3: Detect problem type")
    problem = generator._detect_problem_type({
        "fix_description": "tight coupling between modules"
    })
    print(f"  Detected: {problem}")
    assert problem is not None
    print("  ✅ Test 3 passed")
    
    print("\n✅ ArchitectureSolutionGenerator tests passed!")


if __name__ == "__main__":
    print("="*60)
    print("Running Phase 2 & 3 Integration Tests")
    print("="*60)
    
    try:
        test_rule_recommender()
        test_effectiveness_tracker()
        test_skill_generator()
        test_architecture_generator()
        
        print("\n" + "="*60)
        print("🎉 All Phase 2 & 3 tests passed!")
        print("="*60)
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
