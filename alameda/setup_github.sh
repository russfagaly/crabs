#!/bin/bash
# setup_github.sh — One-time GitHub Pages setup for Alameda 12u All-Stars
# Run this from the 12u_AllStars folder on your own computer.
# Usage: bash setup_github.sh

set -e

GITHUB_USER="russfagaly"
GITHUB_TOKEN="YOUR_TOKEN_HERE"  # paste your token here, never commit this file
REPO_NAME="crabs"
REMOTE="https://${GITHUB_USER}:${GITHUB_TOKEN}@github.com/${GITHUB_USER}/${REPO_NAME}.git"

echo "▶ Creating GitHub repository..."
curl -s -X POST https://api.github.com/user/repos \
  -H "Authorization: token ${GITHUB_TOKEN}" \
  -H "Accept: application/vnd.github.v3+json" \
  -d "{\"name\":\"${REPO_NAME}\",\"description\":\"2026 Alameda 12u All-Stars Stats Dashboard\",\"private\":false,\"auto_init\":false}" \
  > /tmp/gh_create.json
echo "  Done."

echo "▶ Copying dashboard.html → index.html (GitHub Pages serves index.html by default)..."
cp dashboard.html index.html

echo "▶ Initializing git repo..."
git init
git add .
git commit -m "Initial commit — 2026 Alameda 12u All-Stars dashboard"
git branch -M main

echo "▶ Pushing to GitHub..."
git remote add origin "${REMOTE}"
git push -u origin main

echo "▶ Enabling GitHub Pages..."
curl -s -X POST "https://api.github.com/repos/${GITHUB_USER}/${REPO_NAME}/pages" \
  -H "Authorization: token ${GITHUB_TOKEN}" \
  -H "Accept: application/vnd.github.v3+json" \
  -d '{"source":{"branch":"main","path":"/"}}'

echo ""
echo "✅ Done! Your dashboard will be live at:"
echo "   https://${GITHUB_USER}.github.io/${REPO_NAME}/"
echo ""
echo "   (GitHub Pages takes ~60 seconds to go live on first deploy)"
echo ""
echo "▶ To update the dashboard after future games, run:"
echo "   bash update_github.sh"
