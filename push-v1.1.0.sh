#!/bin/bash
# Push v1.1.0 to GitHub

cd ~/opencode-auto-learning

echo "🚀 Pushing v1.1.0..."

# Push commits
git push origin main

# Push tag
git push origin v1.1.0

echo "✅ Done!"
echo ""
echo "GitHub: https://github.com/Jasonbr/opencode-auto-learning"
