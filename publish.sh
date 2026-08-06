#!/bin/bash
# publish.sh — rebuild the multi-team hub, encrypt every page, and push live.
#
#   Usage:  export STATICRYPT_PASSWORD="Wally4President"
#           bash publish.sh
#
# What it does:
#   1. Runs build_hub.py (regenerates each team dashboard + game pages,
#      injects the centered "Home" switcher, rebuilds the hub landing).
#   2. Encrypts the hub + every team page with StatiCrypt (one shared salt,
#      so a single password unlock covers the whole site).
#   3. Safety-checks that nothing is left in plaintext, then commits + pushes.
#   4. Verifies the change actually reached the live site, by comparing the
#      served bytes against HEAD. Exits non-zero if the site is still stale.
#
# Step 4 exists because a green `git push` proved nothing: on 2026-08-06 three
# publishes pushed fine while GitHub Pages failed every build, and this script
# reported "✅ Live" all three times to a site that was five weeks out of date.
#
# Requires: python3, node/npx, curl, and git push access (configure a credential
# helper or a token in the remote URL once). `gh` is optional — used to read the
# deploy workflow's conclusion; without it, verification falls back to the
# served-bytes comparison alone.
set -e
cd "$(dirname "$0")"

if [ -z "$STATICRYPT_PASSWORD" ]; then
  echo "ERROR: STATICRYPT_PASSWORD not set — refusing (would publish UNENCRYPTED)." >&2
  echo '   Run:  export STATICRYPT_PASSWORD="Wally4President"   then re-run.' >&2
  exit 1
fi
command -v npx >/dev/null 2>&1 || { echo "ERROR: node/npx required for StatiCrypt." >&2; exit 1; }

echo "▶ 1/3  Regenerating all teams + hub..."
python3 build_hub.py

echo "▶ 2/3  Encrypting (shared salt = single login)..."
SALT='{"salt":"a793b1e16bd36057b6679fa4e990a233"}'
# ENC — encrypt the given .html files, SKIPPING any that are already encrypted.
#
# This guard is essential. Team pages are safe without it because build_hub.py
# rewrites them as fresh plaintext on every run, so each encryption starts from
# plaintext. The scouting reports in scouting/ have no generator — they are
# static, hand-authored files. Without this guard every publish re-encrypted the
# previous ciphertext, nesting a new layer and ~doubling the file each time
# (60 KB -> 50 MB over nine publishes, which eventually crashed node).
ENC() {
  local files=() rest=() f expect_val=0
  for f in "$@"; do
    if [ $expect_val -eq 1 ]; then rest+=("$f"); expect_val=0; continue; fi
    case "$f" in
      -*) rest+=("$f"); expect_val=1 ;;
      *)  if grep -q "staticrypt" "$f" 2>/dev/null; then
            echo "      skip (already encrypted): $f"
          else
            files+=("$f")
          fi ;;
    esac
  done
  if [ ${#files[@]} -eq 0 ]; then return 0; fi
  npx --yes staticrypt@3 "${files[@]}" "${rest[@]}" -c .staticrypt.json --remember 365 --short >/dev/null 2>&1
}
echo "$SALT" > .staticrypt.json
ENC index.html -d .
# auto-detect team folders (any dir with a pipeline/ and an index.html)
for d in */ ; do
  t=${d%/}
  [ -f "$t/index.html" ] && [ -d "$t/pipeline" ] || continue
  echo "    · $t"
  echo "$SALT" > "$t/.staticrypt.json"
  ENC "$t/index.html" "$t/dashboard.html" -d "$t"
  [ -f "$t/scouting.html" ] && ENC "$t/scouting.html" -d "$t"
  if ls "$t"/games/*.html >/dev/null 2>&1; then
    echo "$SALT" > "$t/games/.staticrypt.json"
    ENC "$t"/games/*.html -d "$t/games"
  fi
done

# scouting reports (no pipeline/, so encrypt explicitly)
if ls scouting/*.html >/dev/null 2>&1; then
  echo "    · scouting"
  echo "$SALT" > scouting/.staticrypt.json
  ENC scouting/*.html -d scouting
fi

echo "▶ 3/4  Safety check + push..."
# Positive assertion: EVERY .html must carry the staticrypt marker. The old check
# grepped for "<h1>2026", which only matches team pages — a plaintext scouting
# report (<h1>Crabs vs NOLL ...>) would have passed straight through it.
LEAK=""
while IFS= read -r f; do
  grep -q "staticrypt" "$f" || LEAK="${LEAK}${f}"$'\n'
done < <(find . -path ./.git -prune -o -name '*.html' -print)
if [ -n "$LEAK" ]; then
  echo "ERROR: these pages are still UNENCRYPTED — aborting before push:" >&2
  echo "$LEAK" >&2
  exit 1
fi
git add -A
if git diff --cached --quiet; then
  echo "    nothing changed — skipping commit (still verifying what is live)"
else
  git commit -m "Update hub — $(date '+%Y-%m-%d %H:%M')"
  git push
fi

echo "▶ 4/4  Verifying the deploy actually reached the live site..."
# A successful `git push` does NOT mean the site updated. On 2026-08-06, three
# consecutive publishes pushed cleanly while every GitHub Pages build failed, so
# the live site sat five weeks stale while this script cheerfully printed
# "✅ Live" each time. Never claim success without comparing the served bytes.
SITE="https://russfagaly.github.io/crabs/"
WANT=$(git show HEAD:index.html | shasum -a 256 | cut -d' ' -f1)

# Wait for the deploy workflow first, when gh is available — gives a real
# conclusion instead of inferring everything from the served bytes.
if command -v gh >/dev/null 2>&1; then
  for _ in $(seq 1 30); do
    ST=$(gh run list --workflow="Deploy Pages" --limit 1 --json status --jq '.[0].status' 2>/dev/null || echo "")
    [ "$ST" = "completed" ] && break
    sleep 10
  done
  CONC=$(gh run list --workflow="Deploy Pages" --limit 1 --json conclusion --jq '.[0].conclusion' 2>/dev/null || echo "unknown")
  echo "    deploy workflow: ${ST:-unknown} / ${CONC:-unknown}"
fi

for _ in $(seq 1 20); do
  GOT=$(curl -s --max-time 20 "$SITE" | shasum -a 256 | cut -d' ' -f1)
  if [ "$GOT" = "$WANT" ]; then
    echo ""
    echo "✅  VERIFIED LIVE (password-protected) at $SITE"
    echo "    served bytes match HEAD ($(git rev-parse --short HEAD))"
    exit 0
  fi
  sleep 15
done

echo "" >&2
echo "⚠️  PUSHED, BUT NOT LIVE." >&2
echo "    The commit is on origin/main, but $SITE is still serving different" >&2
echo "    bytes than HEAD. The publish did NOT reach users. Check:" >&2
echo "      gh run list --workflow='Deploy Pages'" >&2
echo "      https://www.githubstatus.com   (Actions/Pages outages hit us before)" >&2
exit 4
