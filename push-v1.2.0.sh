#!/bin/bash
# Push v1.2.0 to GitHub

cd ~/opencode-auto-learning

echo "🚀 Pushing v1.2.0 to GitHub..."
echo ""

# Push commits
echo "1. Pushing commits..."
git push origin main

echo ""
echo "2. Creating tag..."
git tag v1.2.0

# Push tag
echo "3. Pushing tag..."
git push origin v1.2.0

echo ""
echo "✅ Done!"
echo ""
echo "GitHub: https://github.com/Jasonbr/opencode-auto-learning"
echo "Release: https://github.com/Jasonbr/opencode-auto-learning/releases/tag/v1.2.0"
