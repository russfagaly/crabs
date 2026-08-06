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
#
# Requires: python3, node/npx, and git push access (configure a credential
# helper or a token in the remote URL once).
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

echo "▶ 3/3  Safety check + push..."
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
if git diff --cached --quiet; then echo "Nothing changed — nothing to push."; exit 0; fi
git commit -m "Update hub — $(date '+%Y-%m-%d %H:%M')"
git push

echo ""
echo "✅  Live (password-protected) at https://russfagaly.github.io/crabs/"
echo "    (GitHub Pages refreshes in ~30-60s)"
