#!/usr/bin/env python3
"""
防套娃规则生效演示
展示在实际 OpenCode 使用中的效果
"""

import sys
import os
import time

sys.path.insert(0, os.path.expanduser('~/opencode-auto-learning/src'))

from rules_integration import (
    RuleTracker,
    RuleRecommender,
    ArchitectureSolutionGenerator
)

def demo_edit_file():
    """演示: 编辑文件时的规则推荐"""
    print("\n" + "=" * 70)
    print("📝 场景: 编辑 src/user_service.py")
    print("=" * 70)
    
    recommender = RuleRecommender()
    
    print("\n[OpenCode] 检测到文件编辑操作")
    time.sleep(0.5)
    print("[OpenCode] 正在分析上下文...")
    time.sleep(0.5)
    
    recs = recommender.recommend_before_edit("src/user_service.py", "edit")
    
    print("\n🔔 智能推荐:")
    print("-" * 70)
    
    for i, r in enumerate(recs, 1):
        auto_apply = "✅" if r['auto_apply'] else "⚠️"
        print(f"\n{i}. [{auto_apply}] {r['rule']}")
        print(f"   权重: {r['weight']:.2f}/1.0")
        print(f"   原因: {r['reason']}")
        print(f"   操作: {'自动应用' if r['auto_apply'] else '建议手动确认'}")
    
    print("\n" + "-" * 70)
    print("💡 提示: 这些推荐基于您的历史执行记录和当前文件类型")

def demo_tdd_flow():
    """演示: TDD 开发流程跟踪"""
    print("\n" + "=" * 70)
    print("🧪 场景: TDD 开发流程")
    print("=" * 70)
    
    tracker = RuleTracker()
    
    steps = [
        ("编写测试", {"test_written_first": True}),
        ("运行测试（失败）", {"test_failed_first": True}),
        ("编写实现代码", {"implementation_minimal": True}),
        ("运行测试（通过）", {"all_tests_pass": True})
    ]
    
    context = {
        "project": "user-service",
        "file": "src/user_service.py",
        "regressions": 0
    }
    
    print("\n跟踪 TDD 执行:")
    print("-" * 70)
    
    for step_name, update in steps:
        context.update(update)
        print(f"\n✓ {step_name}")
        time.sleep(0.3)
    
    result = tracker.track_tdd_execution(context)
    
    print("\n" + "-" * 70)
    if result["content"]["success"]:
        print("✅ TDD 执行完美！已记录到学习系统")
    else:
        print("⚠️  TDD 执行有改进空间")
    
    print(f"\n📊 当前统计:")
    print(f"   总执行次数: {tracker.get_execution_stats()['total']}")

def demo_three_strikes():
    """演示: 3 次失败触发架构方案"""
    print("\n" + "=" * 70)
    print("🚨 场景: 第三次修复失败，自动触发架构方案")
    print("=" * 70)
    
    generator = ArchitectureSolutionGenerator()
    
    print("\n修复历史:")
    print("-" * 70)
    print("尝试 1: 修复 A → 导致 B 失败")
    print("尝试 2: 修复 B → 导致 C 失败")
    print("尝试 3: 修复 C → 导致 A 再次失败")
    
    print("\n" + "-" * 70)
    print("🚨 检测到 3 次失败，自动分析中...")
    time.sleep(1)
    
    failure = {
        "attempt": 3,
        "fix_description": "Fixed A broke B; Fixed B broke C; Fixed C broke A - circular dependency",
        "error_message": "ImportError: circular dependency detected",
        "project": "user-service"
    }
    
    solution = generator.generate_from_three_strikes(failure)
    
    if solution:
        print("\n" + "=" * 70)
        print(f"📋 自动生成架构解决方案")
        print("=" * 70)
        print(f"\n问题类型: {solution['problem_type']}")
        print(f"解决方案: {solution['title']}")
        print(f"预计时间: {solution['estimated_time']}")
        print(f"风险等级: {solution['risk_level']}")
        
        print(f"\n📝 解决步骤:")
        for i, step in enumerate(solution['steps'], 1):
            print(f"\n  {i}. {step['action']}")
            print(f"     💻 {step['command']}")
            print(f"     ✅ {step['verification']}")

def demo_commit_check():
    """演示: 提交前检查"""
    print("\n" + "=" * 70)
    print("📤 场景: 提交前自动检查")
    print("=" * 70)
    
    recommender = RuleRecommender()
    
    changed_files = [
        "src/user_service.py",
        "test_user_service.py",
        "config/database.yaml"
    ]
    
    print("\n变更文件:")
    for f in changed_files:
        print(f"  • {f}")
    
    print("\n" + "-" * 70)
    print("🔍 提交前推荐:")
    
    recs = recommender.recommend_before_commit(changed_files)
    
    for r in recs:
        print(f"\n  ✅ {r['rule']}")
        print(f"     {r['reason']}")
        if r.get('auto_apply'):
            print(f"     🔄 将自动执行")

def main():
    print("\n" + "=" * 70)
    print("🎉 OpenCode 防套娃规则生效演示")
    print("=" * 70)
    print("\n这个演示展示了规则在实际使用中的效果")
    print("=" * 70)
    
    input("\n按 Enter 开始演示...")
    
    demo_edit_file()
    input("\n按 Enter 继续...")
    
    demo_tdd_flow()
    input("\n按 Enter 继续...")
    
    demo_three_strikes()
    input("\n按 Enter 继续...")
    
    demo_commit_check()
    
    print("\n" + "=" * 70)
    print("✅ 演示完成！")
    print("=" * 70)
    print("\n您的 OpenCode 现在拥有:")
    print("  ✅ 编辑前自动推荐规则")
    print("  ✅ TDD 流程自动跟踪")
    print("  ✅ 3次失败自动触发架构方案")
    print("  ✅ 提交前自动检查")
    print("\n🎉 防套娃规则已完全生效！")
    print("=" * 70)

if __name__ == "__main__":
    main()
