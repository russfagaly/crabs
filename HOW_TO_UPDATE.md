# Updating the 2026 All-Stars Hub

Live at **https://russfagaly.github.io/crabs/** (password-protected).
One repo, four tabs, one command to publish.

## Repo layout
```
index.html              ← hub landing (auto-built)
build_hub.py            ← regenerates every team + the hub + switcher
publish.sh              ← build + encrypt + push (run this)
alameda_districts/      ← tab "Alameda Crabs"   (full GC names)
alameda/                ← tab "Crabs Scrimmages" (truncated GC names)
noll/                   ← tab "NOLL"             (First-name Last-initial)
lightning/              ← tab "Lightning"
   <team>/pipeline/     ← roster.py, results.py, generators
   <team>/games/        ← one .py per game
```

## Add a game
1. Put the box-score into a new file `  <team>/games/YYYY_MM_DD_Name.py`
   (copy an existing game in that folder — match its name format exactly;
   the rosters differ per team).
2. Add the game to `  <team>/pipeline/results.py` (GAMES list).

## Publish
```bash
export STATICRYPT_PASSWORD="Wally4President"
bash publish.sh
```
This regenerates all dashboards, rebuilds the hub (records update
automatically), re-encrypts every page under one password, and pushes.
GitHub Pages refreshes in ~30–60s.

## Add a whole new team / rename a tab
Edit the `TEAMS` list at the top of `build_hub.py`, then run `publish.sh`.

## Notes
- `publish.sh` refuses to push if `STATICRYPT_PASSWORD` is unset (so it can
  never publish unencrypted) and aborts if any page is left in plaintext.
- First push needs GitHub auth: when prompted, use username `russfagaly`
  and a personal-access-token (repo scope) as the password — or configure a
  git credential helper once.
