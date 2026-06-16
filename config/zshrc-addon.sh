#!/bin/zsh
# OpenCode Auto-Learning Zsh Addon

# Auto-learning aliases
alias oc-learn='opencode-with-sync'
alias auto-learn='opencode-auto-learn'
alias learn-status='opencode-auto-learn status'
alias mem0-sync='~/bin/opencode-bridge.sh sync'
alias mem0-export='~/bin/opencode-bridge.sh export'
alias mem0-import='~/bin/opencode-bridge.sh import'
alias obsidian-sync='~/bin/obsidian-sync.py sync'

# Enhanced OpenCode function with auto-learning
function opencode-with-sync() {
    export OPENCODE_START_TIME=$(date +%s)
    echo "🚀 Starting OpenCode with Mem0 auto-learning..."
    
    # Start OpenCode
    if command -v opencode &> /dev/null; then
        opencode "$@"
    else
        open "/Applications/OpenCode Dev.app" --args "$@"
    fi
    
    local exit_code=$?
    local duration=$(($(date +%s) - OPENCODE_START_TIME))
    
    # Auto-trigger learning if session > 10 minutes
    if [[ $duration -gt 600 ]]; then
        echo ""
        echo "🧠 Running auto-learning..."
        ~/bin/opencode-auto-learn run 2>&1 | tail -5
    fi
    
    unset OPENCODE_START_TIME
    return $exit_code
}

# Status check on load
echo "🧠 OpenCode Auto-Learning loaded"
echo "   Commands: oc-learn, auto-learn, mem0-sync, obsidian-sync"