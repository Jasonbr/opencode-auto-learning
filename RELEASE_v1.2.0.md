# Release v1.2.0

## 🎉 Major Release: Active Learning + Multimodal Memory

### Phase 4: 主动推荐系统 🤖

**Features:**
- **Context Analysis**: Extract keywords, intent, and entities from user input
- **Multi-dimensional Matching**: Keyword + intent + semantic search
- **Proactive Recommendations**: Automatically suggest relevant memories
- **Smart Ranking**: Rank by relevance score

**Usage:**
```bash
opencode-auto-learn-recommend "部署 Docker 到 Kubernetes"
```

### Phase 5: 智能总结生成 📝

**Features:**
- **Multi-dimensional Summaries**: Executive summary, key decisions, learnings, action items, technical details
- **Multiple Formats**: Markdown, JSON, Text
- **Auto-archive**: Daily/weekly summaries to Obsidian
- **Action Items**: Checkbox-style TODOs

**Usage:**
```bash
opencode-summary              # Last 24 hours
opencode-summary daily        # Daily summary
opencode-summary weekly       # Weekly summary
opencode-summary export json # JSON format
```

### Phase 7: 多模态记忆系统 🖼️💻

**Features:**
- **Image OCR**: Extract text from images
- **Code Indexing**: Auto-detect language, extract functions/classes
- **Multimodal Search**: Search across text, code, and images
- **Automated Workflows**: Auto-capture screenshots and code changes

**Usage:**
```bash
opencode-multimodal image screenshot.png "Architecture"
opencode-multimodal code script.py "Deployment script"
opencode-multimodal search code "docker"
```

## 📊 Complete Feature Matrix

| Feature | Command | Status |
|---------|---------|--------|
| Memory Extraction | `opencode-auto-learn` | ✅ |
| Semantic Search | `opencode-auto-learn semantic-search` | ✅ |
| Knowledge Graph | `opencode-auto-learn build-graph` | ✅ |
| **Active Recommendation** | `opencode-auto-learn-recommend` | ✅ NEW |
| **Session Summary** | `opencode-summary` | ✅ NEW |
| **Image OCR** | `opencode-multimodal image` | ✅ NEW |
| **Code Indexing** | `opencode-multimodal code` | ✅ NEW |
| **Multimodal Search** | `opencode-multimodal search` | ✅ NEW |
| Hermes Sync | `mem0-sync` | ✅ |
| Obsidian Sync | `obsidian-sync` | ✅ |

## 🚀 Installation

```bash
# Clone repository
git clone https://github.com/Jasonbr/opencode-auto-learning.git
cd opencode-auto-learning

# Install
./install.sh

# Configure
source ~/.zshrc
```

## 📚 Documentation

- [Quick Start](docs/tutorial/QUICKSTART.md)
- [API Reference](docs/api/MCP_TOOLS.md)
- [Usage Examples](docs/examples/USAGE_EXAMPLES.md)
- [Enhancement Analysis](docs/ENHANCEMENT_ANALYSIS.md)

## 🎯 System Architecture

```
OpenCode
  ↓ MCP
Mem0 MCP Server
  ├─ Memory Extractor
  ├─ Skill Generator
  ├─ Semantic Search
  ├─ Knowledge Graph
  ├─ Active Recommender ← NEW
  ├─ Session Summarizer ← NEW
  └─ Multimodal Memory  ← NEW
  ↓
Hermes / Obsidian
```

## 🏆 What's Next

According to [ENHANCEMENT_ANALYSIS.md](ENHANCEMENT_ANALYSIS.md):

### Phase 6: Skill Store 🏪
- Community skill sharing
- Version management
- GitHub integration

### Phase 8: Visualization 📊
- Knowledge graph visualization
- Memory timeline
- Dashboard

## 📦 What's Changed

**Added:**
- `src/learning/recommender/proactive_recommender.py`
- `src/learning/summarizer/session_summary.py`
- `src/learning/multimodal/image_ocr.py`
- `src/learning/multimodal/code_indexer.py`
- `scripts/opencode-auto-learn-recommend`
- `scripts/opencode-summary`
- `scripts/opencode-multimodal`
- `CHANGELOG.md`
- Multiple workflow configurations

**Updated:**
- README.md with full feature matrix
- Documentation
- CI/CD configuration

## 🙏 Credits

Built with ❤️ for the OpenCode community.

---

**Full Changelog**: https://github.com/Jasonbr/opencode-auto-learning/compare/v1.0.0...v1.2.0