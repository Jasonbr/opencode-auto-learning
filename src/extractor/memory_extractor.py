#!/usr/bin/env python3
"""
OpenCode 智能记忆提取器
自动从会话中提取关键信息并分类存储
"""

import json
import re
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional

class MemoryExtractor:
    """智能记忆提取器"""
    
    def __init__(self):
        self.memory_dir = Path.home() / ".config/opencode/memory/user"
        self.patterns = self._load_patterns()
    
    def _load_patterns(self) -> Dict:
        """加载提取模式 - 增强版支持技术内容"""
        return {
            "decision": [
                r"决定使用[：:]\s*(.+?)(?:\n|$)",
                r"选择[了]?\s*(.+?)(?:\n|$)",
                r"采用[了]?\s*(.+?)(?:\n|$)",
                r"确定[使用]?\s*(.+?)(?:\n|$)",
            ],
            "learning": [
                r"学习到[：:]\s*(.+?)(?:\n|$)",
                r"发现[了]?\s*(.+?)(?:\n|$)",
                r"原理是[：:]\s*(.+?)(?:\n|$)",
                r"了解[到]?\s*(.+?)(?:\n|$)",
                r"认识到[：:]\s*(.+?)(?:\n|$)",
            ],
            "error-solution": [
                r"错误[：:]\s*(.+?)(?:解决|修复|方案)",
                r"问题[：:]\s*(.+?)(?:解决|修复)",
                r"解决[了]?\s*(.+?)(?:\n|$)",
                r"修复[了]?\s*(.+?)(?:\n|$)",
                r"原因[是：:]\s*(.+?)(?:\n|$)",
            ],
            "pattern": [
                r"模式[：:]\s*(.+?)(?:\n|$)",
                r"规律[：:]\s*(.+?)(?:\n|$)",
                r"通常[：:]\s*(.+?)(?:\n|$)",
                r"一般[：:]\s*(.+?)(?:\n|$)",
                r"习惯[是：:]\s*(.+?)(?:\n|$)",
            ],
            "architecture": [
                r"架构[：:]\s*(.+?)(?:\n|$)",
                r"设计[：:]\s*(.+?)(?:\n|$)",
                r"结构[：:]\s*(.+?)(?:\n|$)",
                r"实现[：:]\s*(.+?)(?:\n|$)",
            ],
            "command": [
                r"```bash\n(.+?)\n```",
                r"```shell\n(.+?)\n```",
                r"```sh\n(.+?)\n```",
            ],
            "config": [
                r"配置[：:]\s*(.+?)(?:\n|$)",
                r"设置[：:]\s*(.+?)(?:\n|$)",
            ],
        }
    
    def extract_from_text(self, text: str) -> List[Dict]:
        """从文本中提取记忆"""
        memories = []
        
        for memory_type, patterns in self.patterns.items():
            for pattern in patterns:
                matches = re.findall(pattern, text, re.IGNORECASE | re.MULTILINE)
                for match in matches:
                    if len(match.strip()) > 10:  # 过滤短句
                        memories.append({
                            "type": memory_type,
                            "content": match.strip(),
                            "extracted_at": datetime.now().isoformat(),
                            "confidence": self._calculate_confidence(match, text)
                        })
        
        return memories
    
    def _calculate_confidence(self, match: str, context: str) -> float:
        """计算置信度"""
        score = 0.5
        
        # 长度检查
        if len(match) > 50:
            score += 0.2
        
        # 完整性检查
        if match.endswith(('。', '.', '！', '!')):
            score += 0.1
        
        # 上下文检查
        if '成功' in context or '完成' in context:
            score += 0.2
        
        return min(score, 1.0)
    
    def save_memory(self, memory: Dict) -> Path:
        """保存记忆到文件"""
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        memory_type = memory["type"]
        
        # 生成文件名
        content_slug = memory["content"][:30].replace(" ", "-").replace("/", "-")
        filename = f"{memory_type}-{timestamp}-{content_slug}.md"
        
        filepath = self.memory_dir / filename
        
        # 写入 Markdown
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"---\n")
            f.write(f"type: {memory_type}\n")
            f.write(f"extracted_at: {memory['extracted_at']}\n")
            f.write(f"confidence: {memory['confidence']:.2f}\n")
            f.write(f"auto_extracted: true\n")
            f.write(f"---\n\n")
            f.write(f"# {memory_type.upper()}\n\n")
            f.write(f"{memory['content']}\n\n")
            f.write(f"## Metadata\n\n")
            f.write(f"- **Type**: {memory_type}\n")
            f.write(f"- **Confidence**: {memory['confidence']:.2%}\n")
            f.write(f"- **Extracted**: {memory['extracted_at']}\n")
        
        return filepath
    
    def process_session(self, session_text: str) -> List[Path]:
        """处理整个会话"""
        memories = self.extract_from_text(session_text)
        saved_files = []
        
        for memory in memories:
            if memory["confidence"] > 0.7:  # 只保存高置信度记忆
                filepath = self.save_memory(memory)
                saved_files.append(filepath)
        
        return saved_files

if __name__ == "__main__":
    import sys
    
    extractor = MemoryExtractor()
    
    if len(sys.argv) > 1:
        # 从文件读取
        with open(sys.argv[1], 'r') as f:
            text = f.read()
    else:
        # 从 stdin 读取
        text = sys.stdin.read()
    
    files = extractor.process_session(text)
    
    print(f"✅ Extracted {len(files)} memories:")
    for f in files:
        print(f"   - {f.name}")
