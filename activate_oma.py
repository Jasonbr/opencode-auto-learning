#!/usr/bin/env python3
"""
oh-my-openagent 防套娃规则激活脚本
在 agent 启动时自动加载
"""

import sys
import os

sys.path.insert(0, os.path.expanduser('~/opencode-auto-learning/src'))

try:
    from rules_integration import (
        RuleTracker,
        RuleRecommender,
        ArchitectureSolutionGenerator
    )
    
    print("✅ Anti-regression rules activated for oh-my-openagent")
    
except Exception as e:
    print(f"⚠️  Rules not loaded: {e}")
