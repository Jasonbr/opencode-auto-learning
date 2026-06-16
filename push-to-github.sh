#!/bin/bash
# Push to GitHub Script

set -e

echo "🚀 Pushing to GitHub..."
echo ""

# Check if remote exists
if git remote | grep -q "origin"; then
    echo "Remote 'origin' already exists"
    echo "Current remotes:"
    git remote -v
else
    echo "Adding remote..."
    git remote add origin https://github.com/Jasonbr/opencode-auto-learning.git
fi

echo ""
echo "Pushing to origin/main..."
git push -u origin main

echo ""
echo "✅ Successfully pushed to GitHub!"
echo ""
echo "Next steps:"
echo "  1. Visit: https://github.com/Jasonbr/opencode-auto-learning"
echo "  2. Create a release: git tag v1.0.0 && git push origin v1.0.0"
echo ""
