# Lafayette Lightning Dashboard — Setup Checklist

## One-time setup

1. **Create GitHub repo** `russfagaly/lightning`
2. **Enable GitHub Pages**: Settings → Pages → Deploy from branch `main`, root `/`
3. **Clone the repo** to your computer, drop these starter files in
4. **Populate `pipeline/roster.py`** from the first box score image
5. **Verify `git remote`** points to `russfagaly/lightning`

## Per-game workflow

1. Get images (hitting-1, hitting-2, pitching) + GC gamelog pasted text
2. Create `games/YYYY_MM_DD_GameName.py` (copy TEMPLATE, fill in stats)
3. Create `games/playlogs/YYYY_MM_DD_GameName.txt` (paste gamelog verbatim)
4. Add entry to `pipeline/results.py`
5. Run `bash update_github.sh`
6. View at https://russfagaly.github.io/lightning/

## Color scheme

Electric yellow `#fbbf24` on dark stormy navy `#0d1520`.
Toggle key in localStorage: `lightning-theme`.

## Reference

See `LAFAYETTE_TECH_SPEC.md` in the Crabs AllStars folder for full
field definitions, IP notation, pQAB rules, GC name truncation, etc.
