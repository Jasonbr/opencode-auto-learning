# OpenCode Auto Learning - 优化与迭代路线图

📅 生成时间: 2026-06-23
📊 系统健康度: 79.2/100 (⚠️ 良好)
🎯 当前版本: v1.1.0

---

## 📋 执行摘要

### 当前状态

| 维度 | 评分 | 状态 |
|------|------|------|
| 记忆质量 | 85 | ✅ 优秀 |
| 技能生成 | 80 | ✅ 良好 |
| 代码质量 | 75 | ⚠️ 需优化 |
| 性能优化 | 70 | ⚠️ 需优化 |
| 安全 | 90 | ✅ 优秀 |
| 可用性 | 75 | ⚠️ 需优化 |

**总体评分: 79.2/100**

### 发现的问题

- **高优先级**: 0 个
- **中优先级**: 1 个 (性能优化)
- **低优先级**: 2 个
- **长期迭代**: 3 个方向

---

## 🚀 Phase 1: 近期优化 (1-2 周)

### 1.1 扩展提取模式 [#1]

**优先级**: 🔴 High  
**影响**: 大幅提升记忆覆盖率  
**工作量**: 低 (2-4 小时)

#### 当前问题
- 只有 8 个基础中文关键词
- learning 类型占比 83%，其他类型捕获不足

#### 优化方案

```python
# 在 memory_extractor.py 中添加更多模式

EXPANDED_PATTERNS = {
    "deployment": [
        r"部署[到]?\s*(.+?)(?:\n|$)",
        r"发布[到]?\s*(.+?)(?:\n|$)",
        r"上线[到]?\s*(.+?)(?:\n|$)",
    ],
    "debugging": [
        r"调试[了]?\s*(.+?)(?:\n|$)",
        r"排查[了]?\s*(.+?)(?:\n|$)",
        r"定位[到]?\s*(.+?)(?:\n|$)",
    ],
    "optimization": [
        r"优化[了]?\s*(.+?)(?:\n|$)",
        r"提升[了]?\s*(.+?)(?:\n|$)",
        r"改进[了]?\s*(.+?)(?:\n|$)",
    ],
    "tool_usage": [
        r"使用\s*(\w+)\s*(.+?)(?:\n|$)",  # 工具使用
        r"通过\s*(\w+)\s*(.+?)(?:\n|$)",   # 通过工具
    ],
    "version": [
        r"升级[到]?\s*(.+?)(?:\n|$)",
        r"降级[到]?\s*(.+?)(?:\n|$)",
        r"版本[为]?\s*(.+?)(?:\n|$)",
    ],
}
```

#### 验收标准
- [ ] learning 类型占比从 83% 降至 60%
- [ ] 新增 deployment/debugging/optimization 类型
- [ ] 每类记忆数 > 50

---

### 1.2 命令去重与泛化 [#2]

**优先级**: 🔴 High  
**影响**: 减少技能重复，提升实用性  
**工作量**: 中 (4-8 小时)

#### 当前问题
- 相同命令重复出现 (如 `sudo systemctl restart siriusec` 出现多次)
- 硬编码路径 (`/Users/xiaoxi/`) 降低可移植性

#### 优化方案

```python
# 添加到 skill_generator.py

class CommandNormalizer:
    """命令标准化"""
    
    @staticmethod
    def normalize(cmd: str) -> str:
        """标准化命令用于比较"""
        # 替换用户路径
        cmd = re.sub(r'/Users/\w+', '$HOME', cmd)
        cmd = re.sub(r'/home/\w+', '$HOME', cmd)
        
        # 替换时间戳
        cmd = re.sub(r'\d{4}-\d{2}-\d{2}', 'YYYY-MM-DD', cmd)
        cmd = re.sub(r'\d{2}:\d{2}:\d{2}', 'HH:MM:SS', cmd)
        
        # 替换动态 ID
        cmd = re.sub(r'\b[0-9a-f]{8}\b', '<ID>', cmd)
        
        return cmd.strip()
    
    @staticmethod
    def similarity(cmd1: str, cmd2: str) -> float:
        """计算命令相似度 (0-1)"""
        from difflib import SequenceMatcher
        return SequenceMatcher(None, cmd1, cmd2).ratio()

# 在生成技能时使用
commands = [...]  # 原始命令
normalized = [(cmd, self.normalize(cmd)) for cmd in commands]

# 去重：相似度 > 0.8 视为重复
unique_commands = []
for cmd, norm in normalized:
    is_duplicate = any(
        self.similarity(norm, existing_norm) > 0.8 
        for _, existing_norm in unique_commands
    )
    if not is_duplicate:
        unique_commands.append((cmd, norm))
```

#### 验收标准
- [ ] 重复命令减少 50%+
- [ ] 生成的技能中 $HOME 替代硬编码路径
- [ ] 技能文件大小减少 30%

---

### 1.3 增强日志记录 [#3]

**优先级**: 🟡 Medium  
**影响**: 便于调试和监控  
**工作量**: 低 (1-2 小时)

#### 优化方案

```bash
# 在 opencode-auto-learn 中添加日志

LOG_FILE="$HOME/.config/opencode/logs/auto-learning.log"
mkdir -p "$(dirname "$LOG_FILE")"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "INFO: Starting auto-learning workflow"
log "INFO: Found $SESSION_COUNT sessions"

# 错误处理
set -o pipefail
trap 'log "ERROR: Exit code $? at line $LINENO"' ERR
```

---

## 🔧 Phase 2: 中期优化 (2-4 周)

### 2.1 记忆分层存储 [#4]

**优先级**: 🟡 Medium  
**影响**: 提升性能和可维护性  
**工作量**: 中 (8-16 小时)

#### 当前问题
- 1,297 条记忆全部在 `memory/user/` 单目录
- 文件过多影响文件系统性能

#### 优化方案

```
memory/
├── user/
│   └── (保持现有结构，但限制为最近 90 天)
├── archived/
│   ├── 2024-04/
│   ├── 2024-05/
│   └── 2024-06/
└── index.db  # SQLite 元数据索引
```

```python
# memory_manager.py

class MemoryManager:
    def __init__(self):
        self.active_dir = Path.home() / ".config/opencode/memory/user"
        self.archive_dir = Path.home() / ".config/opencode/memory/archived"
        self.db = sqlite3.connect("memory/index.db")
        
    def archive_old_memories(self, days: int = 90):
        """归档旧记忆"""
        cutoff = datetime.now() - timedelta(days=days)
        
        for memory_file in self.active_dir.glob("*.md"):
            mtime = datetime.fromtimestamp(memory_file.stat().st_mtime)
            if mtime < cutoff:
                # 移动到归档
                month_dir = self.archive_dir / mtime.strftime("%Y-%m")
                month_dir.mkdir(exist_ok=True)
                memory_file.rename(month_dir / memory_file.name)
    
    def search(self, query: str) -> List[Dict]:
        """搜索记忆（包含归档）"""
        # 先从索引查找
        results = self.db.execute(
            "SELECT * FROM memories WHERE content LIKE ?",
            (f"%{query}%",)
        ).fetchall()
        
        # 返回记忆文件路径
        return [self._get_memory_path(r) for r in results]
```

#### 验收标准
- [ ] active 目录记忆 < 300
- [ ] 搜索性能提升 50%
- [ ] 自动归档功能运行

---

### 2.2 多维度记忆评分 [#5]

**优先级**: 🟡 Medium  
**影响**: 提升记忆质量  
**工作量**: 中 (8-12 小时)

#### 优化方案

```python
# memory_scorer.py

class MemoryScorer:
    """多维度记忆评分"""
    
    def score(self, memory: Dict) -> Dict[str, float]:
        scores = {}
        
        # 完整性 (是否有问题+解决方案)
        content = memory.get('content', '')
        has_problem = bool(re.search(r'(问题|错误|bug|issue)', content, re.I))
        has_solution = bool(re.search(r'(解决|修复|方案|fix)', content, re.I))
        scores['completeness'] = 1.0 if (has_problem and has_solution) else 0.5
        
        # 可复用性 (是否通用)
        specific_terms = ['xiaoxi', 'siriusec', 'project_x']
        specific_count = sum(1 for term in specific_terms if term in content)
        scores['reusability'] = 1.0 - (specific_count * 0.2)
        
        # 时效性 (技术栈是否过时)
        outdated_terms = ['python2', 'vue2', 'angularjs']
        outdated_count = sum(1 for term in outdated_terms if term in content.lower())
        scores['freshness'] = 1.0 - (outdated_count * 0.3)
        
        # 准确性 (基于验证状态)
        scores['accuracy'] = 1.0 if '#verified' in content else 0.7
        
        # 综合评分
        scores['overall'] = sum(scores.values()) / len(scores)
        
        return scores
    
    def auto_tag(self, memory: Dict) -> List[str]:
        """自动打标签"""
        tags = []
        content = memory.get('content', '')
        
        scores = self.score(memory)
        
        if scores['overall'] > 0.8:
            tags.append('#high-quality')
        elif scores['overall'] < 0.5:
            tags.append('#needs-review')
        
        if scores['freshness'] < 0.5:
            tags.append('#deprecated')
        
        if scores['reusability'] > 0.8:
            tags.append('#reusable')
        
        return tags
```

---

## 🎯 Phase 3: 长期迭代 (1-2 月)

### 3.1 向量嵌入升级 [#6] ⭐ 优先级最高

**优先级**: 🔴 Critical  
**影响**: 质的飞跃 - 语义理解能力  
**工作量**: 高 (20-40 小时)

#### 当前问题
- 使用 MD5 哈希嵌入，语义理解能力差
- 无法实现真正的语义相似度匹配

#### 优化方案

```python
# enhanced_embedder.py

from sentence_transformers import SentenceTransformer
import numpy as np

class SemanticEmbedder:
    """语义嵌入 - 使用 sentence-transformers"""
    
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        # 本地模型，无需 API
        self.model = SentenceTransformer(model_name)
        self.dim = 384  # all-MiniLM-L6-v2 输出维度
    
    def embed(self, text: str) -> np.ndarray:
        """生成语义向量"""
        return self.model.encode(text, normalize_embeddings=True)
    
    def similarity(self, text1: str, text2: str) -> float:
        """计算语义相似度"""
        emb1 = self.embed(text1)
        emb2 = self.embed(text2)
        return float(np.dot(emb1, emb2))

# 迁移到 pgvector (PostgreSQL)

class VectorStore:
    """向量数据库存储"""
    
    def __init__(self, db_url: str = "postgresql://localhost/memories"):
        import psycopg2
        self.conn = psycopg2.connect(db_url)
        
    def init_db(self):
        """初始化向量表"""
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS memory_vectors (
                id SERIAL PRIMARY KEY,
                content TEXT,
                embedding vector(384),
                metadata JSONB,
                created_at TIMESTAMP DEFAULT NOW()
            )
        """)
        
        # 创建 HNSW 索引 (快速近似最近邻)
        self.conn.execute("""
            CREATE INDEX ON memory_vectors 
            USING hnsw (embedding vector_cosine_ops)
            WITH (m = 16, ef_construction = 64)
        """)
    
    def search(self, query: str, top_k: int = 5) -> List[Dict]:
        """语义搜索"""
        embedder = SemanticEmbedder()
        query_vec = embedder.embed(query)
        
        results = self.conn.execute("""
            SELECT content, metadata, 
                   1 - (embedding <=> %s::vector) as similarity
            FROM memory_vectors
            ORDER BY embedding <=> %s::vector
            LIMIT %s
        """, (query_vec, query_vec, top_k)).fetchall()
        
        return results
```

#### 验收标准
- [ ] 语义搜索准确率 > 80%
- [ ] 搜索延迟 < 100ms
- [ ] 支持跨语言语义匹配

---

### 3.2 交互式 TUI 界面 [#7]

**优先级**: 🟡 Medium  
**影响**: 提升用户体验  
**工作量**: 高 (16-32 小时)

#### 技术选型

```python
# requirements.txt
rich>=13.0.0
prompt-toolkit>=3.0.0
textual>=0.41.0
```

#### 界面设计

```python
# tui.py

from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, DataTable, Static, Input
from textual.containers import Container, Horizontal

class MemoryBrowser(App):
    """记忆浏览器 TUI"""
    
    CSS = """
    Screen { align: center middle; }
    #memory-table { height: 80%; }
    """
    
    def compose(self) -> ComposeResult:
        yield Header()
        
        with Container():
            yield Input(placeholder="搜索记忆...", id="search")
            yield DataTable(id="memory-table")
        
        yield Footer()
    
    def on_mount(self) -> None:
        table = self.query_one("#memory-table", DataTable)
        table.add_columns("Type", "Date", "Preview", "Score")
        self.load_memories()
    
    def load_memories(self, filter_text: str = ""):
        """加载记忆列表"""
        memories = self.search_memories(filter_text)
        
        table = self.query_one("#memory-table", DataTable)
        table.clear()
        
        for mem in memories:
            table.add_row(
                mem['type'],
                mem['date'][:10],
                mem['content'][:50] + "...",
                f"{mem['score']:.2f}"
            )
    
    def on_input_changed(self, event: Input.Changed) -> None:
        """实时搜索"""
        self.load_memories(event.value)

if __name__ == "__main__":
    app = MemoryBrowser()
    app.run()
```

---

### 3.3 知识图谱可视化 [#8]

**优先级**: 🟢 Low  
**影响**: 直观展示记忆关联  
**工作量**: 高 (16-24 小时)

#### 方案

```python
# graph_visualizer.py

import networkx as nx
from pyvis.network import Network

def visualize_graph(memories: List[Dict], output_file: str = "graph.html"):
    """生成交互式知识图谱"""
    
    G = nx.Graph()
    
    # 添加节点
    for mem in memories:
        G.add_node(
            mem['id'],
            label=mem['title'][:20],
            title=mem['content'][:100],
            group=mem['type']
        )
    
    # 添加边（基于关键词共现）
    for i, mem1 in enumerate(memories):
        for mem2 in memories[i+1:]:
            similarity = calculate_similarity(mem1, mem2)
            if similarity > 0.5:
                G.add_edge(
                    mem1['id'], mem2['id'],
                    weight=similarity
                )
    
    # 生成可视化
    net = Network(height="800px", width="100%", bgcolor="#222222", font_color="white")
    net.from_nx(G)
    
    # 按类型着色
    type_colors = {
        'command': '#ff6b6b',
        'learning': '#4ecdc4',
        'decision': '#45b7d1',
        'error-solution': '#f9ca24',
        'config': '#6c5ce7'
    }
    
    for node in net.nodes:
        node['color'] = type_colors.get(node.get('group'), '#95a5a6')
    
    net.save_graph(output_file)
    print(f"图谱已保存: {output_file}")
```

---

## 📊 优先级矩阵

```
影响 ↑
    │
高  │  [3.1 向量升级]      [1.1 提取模式]
    │  [6 记忆评分]        [1.2 命令去重]
    │
中  │  [3.2 TUI]          [2.1 分层存储]
    │  [3.3 可视化]        [2.2 评分系统]
    │
低  │                      [1.3 日志增强]
    │
    └────────────────────────────────→ 工作量
         低              中              高
```

---

## 🎯 推荐执行顺序

### 第 1 周: 快速收益
1. ✅ **1.1 扩展提取模式** - 提升记忆覆盖率
2. ✅ **1.2 命令去重** - 提升技能质量
3. ✅ **1.3 日志增强** - 便于调试

### 第 2-4 周: 核心优化
4. 🔄 **2.1 分层存储** - 性能优化
5. 🔄 **2.2 记忆评分** - 质量提升

### 第 2 月: 质的飞跃
6. ⭐ **3.1 向量升级** - 最重要的改进
7. 🎨 **3.2 TUI 界面** - 用户体验

---

## 📈 预期收益

| 优化项 | 预期收益 | 成功指标 |
|--------|----------|----------|
| 扩展提取模式 | 记忆类型平衡 | learning < 60% |
| 命令去重 | 减少重复 | 技能大小 -30% |
| 分层存储 | 搜索提速 | < 300ms |
| 向量升级 | 语义理解 | 准确率 > 80% |
| TUI 界面 | 使用便捷 | 交互式浏览 |

---

## 🔗 相关资源

- **GitHub**: https://github.com/Jasonbr/opencode-auto-learning
- **Release**: https://github.com/Jasonbr/opencode-auto-learning/releases/tag/v1.1.0
- **Documentation**: README.md

---

*最后更新: 2026-06-23*
