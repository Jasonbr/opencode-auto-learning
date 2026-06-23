#!/bin/bash
# Hermes ↔ OpenCode 记忆桥接

PYTHON=~/.venvs/mem0/bin/python
SCRIPT=~/bin/opencode-hermes-bridge.py

case "$1" in
    export)
        $PYTHON $SCRIPT export
        ;;
    import)
        $PYTHON $SCRIPT import
        ;;
    sync)
        $PYTHON $SCRIPT sync
        ;;
    summary)
        $PYTHON $SCRIPT summary
        ;;
    *)
        echo "Usage: $0 {export|import|sync|summary}"
        exit 1
        ;;
esac
