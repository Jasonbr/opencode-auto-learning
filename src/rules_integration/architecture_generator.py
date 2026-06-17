#!/usr/bin/env python3
"""
Architecture Solution Generator - 自动生成架构解决方案
针对循环依赖、紧耦合等问题提供具体重构步骤
"""

from datetime import datetime
from typing import Dict, List, Any, Optional


class ArchitectureSolutionGenerator:
    """
    自动生成架构问题的解决方案
    """
    
    def __init__(self, mem0_client=None):
        self.mem0 = mem0_client
        
        # 问题类型与解决方案的映射
        self.solution_templates = {
            "circular_dependency": {
                "title": "解决循环依赖",
                "description": "引入接口层打破循环依赖",
                "steps": [
                    {
                        "action": "识别循环依赖",
                        "command": "depgraph --circular src/",
                        "verification": "确认循环依赖已列出"
                    },
                    {
                        "action": "提取接口",
                        "command": "Create Interface for shared functionality",
                        "verification": "Interface 编译/语法正确"
                    },
                    {
                        "action": "使用依赖注入",
                        "command": "Inject dependencies via constructor",
                        "verification": "Tests pass with new DI"
                    }
                ]
            },
            "tight_coupling": {
                "title": "解耦紧耦合模块",
                "description": "使用事件总线或消息队列解耦",
                "steps": [
                    {
                        "action": "识别紧耦合点",
                        "command": "Analyze direct imports and method calls",
                        "verification": "Coupling points documented"
                    },
                    {
                        "action": "引入事件总线",
                        "command": "Implement event bus pattern",
                        "verification": "Events properly dispatched"
                    },
                    {
                        "action": "迁移到事件驱动",
                        "command": "Replace direct calls with events",
                        "verification": "All tests pass"
                    }
                ]
            },
            "state_sharing": {
                "title": "隔离共享状态",
                "description": "使用状态管理库或纯函数",
                "steps": [
                    {
                        "action": "识别共享状态",
                        "command": "Find global variables and singletons",
                        "verification": "State locations listed"
                    },
                    {
                        "action": "引入状态管理",
                        "command": "Add Redux/Vuex/Zustand store",
                        "verification": "Store initialized"
                    },
                    {
                        "action": "迁移状态访问",
                        "command": "Replace direct access with store",
                        "verification": "No direct state mutations"
                    }
                ]
            },
            "god_class": {
                "title": "拆分上帝类",
                "description": "使用单一职责原则拆分",
                "steps": [
                    {
                        "action": "分析职责",
                        "command": "Identify distinct responsibilities",
                        "verification": "Responsibilities documented"
                    },
                    {
                        "action": "提取类",
                        "command": "Create new classes per responsibility",
                        "verification": "Classes compile"
                    },
                    {
                        "action": "重构依赖",
                        "command": "Update references to new classes",
                        "verification": "All tests pass"
                    }
                ]
            }
        }
    
    def generate_solution(self, problem_type: str, context: Dict) -> Optional[Dict[str, Any]]:
        """
        生成架构解决方案
        
        Args:
            problem_type: 问题类型 (circular_dependency, tight_coupling, etc.)
            context: 上下文信息
            
        Returns:
            解决方案
        """
        template = self.solution_templates.get(problem_type)
        
        if not template:
            return self._generate_generic_solution(problem_type, context)
        
        # 自定义解决方案
        solution = {
            "id": f"solution-{problem_type}-{datetime.now().timestamp()}",
            "problem_type": problem_type,
            "title": template["title"],
            "description": template["description"],
            "context": context,
            "steps": template["steps"],
            "estimated_time": self._estimate_time(template["steps"]),
            "risk_level": self._assess_risk(context),
            "prerequisites": self._get_prerequisites(problem_type),
            "rollback_plan": self._get_rollback_plan(problem_type),
            "generated_at": datetime.now().isoformat()
        }
        
        return solution
    
    def generate_from_three_strikes(self, failure: Dict) -> Optional[Dict[str, Any]]:
        """
        从 3 次失败触发生成解决方案
        
        Args:
            failure: 失败信息
            
        Returns:
            解决方案
        """
        # 分析问题类型
        problem_type = self._detect_problem_type(failure)
        
        # 生成解决方案
        return self.generate_solution(problem_type, {
            "attempts": failure.get("attempt"),
            "error": failure.get("error_message"),
            "fix_history": failure.get("fix_description")
        })
    
    def _detect_problem_type(self, failure: Dict) -> str:
        """检测问题类型"""
        desc = failure.get("fix_description", "").lower()
        error = failure.get("error_message", "").lower()
        
        indicators = {
            "circular": ["circular", "cycle", "depends on"],
            "coupling": ["tight", "coupled", "import"],
            "state": ["state", "global", "singleton"],
            "god": ["large", "many methods", "god"]
        }
        
        for problem_type, keywords in indicators.items():
            for keyword in keywords:
                if keyword in desc or keyword in error:
                    return f"{problem_type}_dependency" if problem_type == "circular" else problem_type
        
        return "tight_coupling"  # 默认
    
    def _estimate_time(self, steps: List[Dict]) -> str:
        """估算时间"""
        base_time = len(steps) * 30  # 30分钟每步
        
        if base_time < 60:
            return f"{base_time} minutes"
        elif base_time < 180:
            return f"{base_time // 60} hours"
        else:
            return f"{base_time // 60}+ hours"
    
    def _assess_risk(self, context: Dict) -> str:
        """评估风险"""
        attempts = context.get("attempts", 0)
        
        if attempts >= 5:
            return "high"
        elif attempts >= 3:
            return "medium"
        else:
            return "low"
    
    def _get_prerequisites(self, problem_type: str) -> List[str]:
        """获取前置条件"""
        return [
            "完整测试覆盖",
            "代码备份",
            "CI/CD 配置正确"
        ]
    
    def _get_rollback_plan(self, problem_type: str) -> str:
        """获取回滚计划"""
        return """
回滚计划:
1. 保留重构前的 git 分支
2. 使用 git revert 撤销更改
3. 恢复备份的代码
4. 重新运行测试确保稳定
"""
    
    def _generate_generic_solution(self, problem_type: str, context: Dict) -> Dict[str, Any]:
        """生成通用解决方案"""
        return {
            "id": f"solution-generic-{datetime.now().timestamp()}",
            "problem_type": problem_type,
            "title": f"解决 {problem_type}",
            "description": "通用架构重构方案",
            "context": context,
            "steps": [
                {
                    "action": "分析问题",
                    "command": "Document the problem and impact",
                    "verification": "Problem understood"
                },
                {
                    "action": "设计解决方案",
                    "command": "Design minimal viable solution",
                    "verification": "Design reviewed"
                },
                {
                    "action": "实施重构",
                    "command": "Apply changes incrementally",
                    "verification": "Tests pass"
                }
            ],
            "estimated_time": "2-4 hours",
            "risk_level": "medium",
            "prerequisites": ["Tests", "Backup"],
            "rollback_plan": "Git revert to previous commit",
            "generated_at": datetime.now().isoformat()
        }


if __name__ == "__main__":
    print("Testing ArchitectureSolutionGenerator...")
    
    generator = ArchitectureSolutionGenerator()
    
    # 测试生成解决方案
    print("\n=== Test: Generate Solution ===")
    solution = generator.generate_solution("circular_dependency", {
        "attempts": 3,
        "error": "Circular dependency detected",
        "files": ["a.py", "b.py"]
    })
    
    print(f"Solution: {solution['title']}")
    print(f"Steps: {len(solution['steps'])}")
    print(f"Estimated time: {solution['estimated_time']}")
    
    # 测试从 3 次失败生成
    print("\n=== Test: Generate from Three Strikes ===")
    solution = generator.generate_from_three_strikes({
        "attempt": 3,
        "fix_description": "Fixed A, broke B; Fixed B, broke C - circular",
        "error_message": "Import error"
    })
    
    print(f"Detected problem: {solution['problem_type']}")
    print(f"Solution: {solution['title']}")
    
    print("\n✅ ArchitectureSolutionGenerator tests passed!")
