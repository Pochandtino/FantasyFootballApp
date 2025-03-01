import itertools
import json
import pandas as pd

# Load team data from JSON
with open("data/league_standings_latest.json", "r") as f:
    league_standings = json.load(f)

# Extract team names and IDs
teams = [team['Team Name'] for team in league_standings]

# Allow user to define gameweeks for matches
define_gameweeks = [5, 7, 9, 11, 13, 15]  # Example custom selection

# Generate round-robin fixtures
def generate_fixtures(teams, gameweeks):
    fixtures = []
    round_robin = list(itertools.combinations(teams, 2))  # All possible matchups
    
    for i, matchup in enumerate(round_robin):
        gameweek = gameweeks[i % len(gameweeks)]  # Rotate through selected gameweeks
        fixtures.append({
            "Gameweek": gameweek,
            "Home": matchup[0],
            "Away": matchup[1]
        })
    
    return fixtures

# Generate fixtures
fixtures = generate_fixtures(teams, define_gameweeks)

# Save fixtures to JSON
with open("data/fixtures.json", "w") as f:
    json.dump(fixtures, f, indent=4)

print("Fixtures generated and saved to data/fixtures.json")
