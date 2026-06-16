#!/bin/bash
# OpenCode Auto-Learning System Installer

set -e

echo "🧠 OpenCode Auto-Learning System Installer"
echo "========================================="
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Check prerequisites
echo "📋 Checking prerequisites..."

if ! command -v python3 &> /dev/null; then
    echo -e "${RED}✗ Python 3 is required${NC}"
    exit 1
fi

if ! command -v opencode &> /dev/null; then
    echo -e "${YELLOW}⚠ OpenCode not found. Please install first.${NC}"
fi

echo -e "${GREEN}✓ Prerequisites check passed${NC}"
echo ""

# Create directories
echo "📁 Creating directories..."
mkdir -p ~/.config/opencode/mcp-servers
mkdir -p ~/.config/opencode/skills/auto-learning/{extractor,generator,vector,graph}
mkdir -p ~/.config/opencode/workflows
mkdir -p ~/.config/opencode/scripts
mkdir -p ~/bin
mkdir -p ~/.mem0

echo -e "${GREEN}✓ Directories created${NC}"
echo ""

# Install Python dependencies
echo "📦 Installing Python dependencies..."
python3 -m pip install -q pyyaml sqlite3 || echo "Note: Some packages may already be installed"
echo -e "${GREEN}✓ Dependencies installed${NC}"
echo ""

# Copy files
echo "📂 Installing files..."

# MCP Server
cp src/mcp/mem0_mcp_server.py ~/.config/opencode/mcp-servers/
cp src/mcp/mem0_wrapper.sh ~/.config/opencode/mcp-servers/
chmod +x ~/.config/opencode/mcp-servers/mem0_wrapper.sh

# Learning modules
cp src/learning/extractor/memory_extractor.py ~/.config/opencode/skills/auto-learning/extractor/
cp src/learning/generator/skill_generator.py ~/.config/opencode/skills/auto-learning/generator/
cp src/learning/vector/semantic_search.py ~/.config/opencode/skills/auto-learning/vector/
cp src/learning/graph/knowledge_graph.py ~/.config/opencode/skills/auto-learning/graph/
chmod +x ~/.config/opencode/skills/auto-learning/*/*.py

# Bridge tools
cp src/bridge/opencode-hermes-bridge.py ~/bin/
cp src/bridge/opencode-bridge.sh ~/bin/
cp src/bridge/obsidian-sync.py ~/bin/
chmod +x ~/bin/opencode-bridge.sh
chmod +x ~/bin/obsidian-sync.py

# CLI tool
cp scripts/opencode-auto-learn ~/bin/
chmod +x ~/bin/opencode-auto-learn

echo -e "${GREEN}✓ Files installed${NC}"
echo ""

# Configure OpenCode
echo "⚙️ Configuring OpenCode..."
if [ -f ~/.config/opencode/opencode.json ]; then
    if ! grep -q "mem0-memory" ~/.config/opencode/opencode.json; then
        echo -e "${YELLOW}⚠ Please add mem0-memory MCP configuration manually${NC}"
        echo "  See: config/opencode-mcp-config.json"
    else
        echo -e "${GREEN}✓ OpenCode MCP already configured${NC}"
    fi
else
    echo -e "${YELLOW}⚠ OpenCode config not found${NC}"
fi
echo ""

# Add to .zshrc
echo "🔧 Configuring shell..."
if ! grep -q "opencode-auto-learning" ~/.zshrc 2>/dev/null; then
    cp config/zshrc-addon.sh ~/.opencode-auto-learning-zshrc.sh
    echo "source ~/.opencode-auto-learning-zshrc.sh" >> ~/.zshrc
    echo -e "${GREEN}✓ Added to .zshrc${NC}"
else
    echo -e "${YELLOW}⚠ Already configured in .zshrc${NC}"
fi
echo ""

# Create Launchd service
echo "🚀 Creating Launchd service..."
mkdir -p ~/Library/LaunchAgents
cp config/com.mem0.sync.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.mem0.sync.plist 2>/dev/null || true
echo -e "${GREEN}✓ Launchd service created${NC}"
echo ""

# Summary
echo "========================================="
echo -e "${GREEN}✅ Installation complete!${NC}"
echo ""
echo "Next steps:"
echo "  1. Restart your terminal or run: source ~/.zshrc"
echo "  2. Configure OpenCode MCP (see config/opencode-mcp-config.json)"
echo "  3. Restart OpenCode"
echo "  4. Test: opencode-auto-learn status"
echo ""
echo "Available commands:"
echo "  oc-learn              - Start OpenCode with auto-learning"
echo "  opencode-auto-learn   - Manual learning trigger"
echo "  mem0-sync             - Sync memories"
echo "  obsidian-sync         - Sync to Obsidian"
echo ""
echo "Documentation:"
echo "  docs/tutorial/QUICKSTART.md"
echo "  docs/api/MCP_TOOLS.md"
echo "========================================="
