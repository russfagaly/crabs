#!/bin/bash
# update_github.sh — Push updated dashboard to GitHub Pages
# Run this after every game (after generate_dashboard.py has been run).
# Usage: bash update_github.sh

set -e

echo "▶ Regenerating dashboard..."
python3 pipeline/generate_dashboard.py

echo "▶ Copying dashboard.html → index.html..."
cp dashboard.html index.html

echo "▶ Pushing to GitHub..."
git add -A
git commit -m "Update dashboard — $(date '+%Y-%m-%d')"
git push

echo ""
echo "✅ Live at: https://russfagaly.github.io/crabs/"
echo "   (allow ~30 seconds for GitHub Pages to refresh)"
