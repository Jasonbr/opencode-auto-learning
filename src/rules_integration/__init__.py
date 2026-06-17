"""
规则集成模块 - 将防套娃规则与自动学习系统集成

Phase 1: Rule Execution Tracking
- RuleTracker: 跟踪规则执行并记录到学习系统
- ViolationAnalyzer: 分析规则违反模式

Phase 2: Proactive Intelligence
- RuleRecommender: 主动推荐相关规则
- EffectivenessTracker: 跟踪规则效果

Phase 3: Smart Skill Generation
- RuleBasedSkillGenerator: 从成功案例生成技能
- ArchitectureSolutionGenerator: 自动生成架构解决方案
"""

from .rule_tracker import RuleTracker
from .violation_analyzer import ViolationAnalyzer
from .rule_recommender import RuleRecommender
from .effectiveness_tracker import EffectivenessTracker
from .skill_generator import RuleBasedSkillGenerator
from .architecture_generator import ArchitectureSolutionGenerator

__version__ = "1.0.0"
__author__ = "Jasonbr"

__all__ = [
    # Phase 1
    "RuleTracker",
    "ViolationAnalyzer",
    
    # Phase 2
    "RuleRecommender",
    "EffectivenessTracker",
    
    # Phase 3
    "RuleBasedSkillGenerator",
    "ArchitectureSolutionGenerator"
]
