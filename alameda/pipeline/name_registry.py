# name_registry.py — 2026 Alameda 12u All-Stars
#
# Maps (jersey_number_string) → display_name
# The display_name must exactly match what appears after the "#" in game files.
# Example: if game file has "Adrien R #6", register ("6",) → "Adrien R"
#
# WHY THIS EXISTS:
# GameChanger scoresheets show player names in "FirstInitial LastName #Jersey" format.
# This registry lets validate.py catch typos or inconsistencies before they corrupt stats.
#
# NICKNAME RULE:
# If a player goes by a nickname, use the nickname here.
# Example: Wallace Beaver goes by "Ace" → register as "Ace B", game files use "Ace B #44"
#
# TRUNCATION RULE:
# GameChanger truncates long first names (e.g. "Sebastian" → "Sebasti...").
# Use the truncated form both here and in game files.
# Example: ("33",) → "Sebasti..."

NAME_REGISTRY = {
    # jersey_str: display_name
    # Fill in once you have your roster and jersey assignments:
    #  "1":  "First L",
    #  "2":  "First L",
    #  ...
}

# Notes on players with known name quirks from the 2026 regular season
# (update if any of these players are on your all-star roster):
KNOWN_QUIRKS = {
    "Adrien Romero":   "Goes by legal name. Game files: 'Adrien R #6'",
    "Robert Fagaly":   "Goes by 'RJ'. Game files: 'RJ F #XX'",
    "Andrew Bryant":   "Goes by 'Drew'. Game files: 'Drew B #4'",
    "Huston Garvine":  "Straightforward. Game files: 'Huston G #20'",
    "Jonah Lee":       "Straightforward. Game files: 'Jonah L #24'",
    "Kai Lin":         "Straightforward. Game files: 'Kai L #11'",
    "Kaleo Pontmayor": "Straightforward. Game files: 'Kaleo P #10'",
    "Roland Hatley":   "Straightforward. Game files: 'Roland H #XX'",
    "Colton Dignon":   "Straightforward. Game files: 'Colton D #19'",
    "Jordan Cerda-Zein":"Hyphenated last name — GameChanger shows as 'Jordan C'. Game files: 'Jordan C #3'",
    "Nico Yuen":       "Straightforward. Game files: 'Nico Y #0'",
    "Orion Mitchell":  "Straightforward. Game files: 'Orion M #XX'",
}
