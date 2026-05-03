#!/bin/bash
echo "🚀 Releasing PROMETHEUS Phase 4 - Month 3"
echo "1. Creating release tag..."
git tag -a v0.3.0 -m "PROMETHEUS Phase 4 - Month 3 Release"
echo "2. Pushing to GitHub..."
git push origin main --tags
echo "✅ Release v0.3.0 created!"
echo "Next: Update GitHub Releases page manually"
