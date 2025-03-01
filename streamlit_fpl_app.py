import itertools
import json
import pandas as pd
import os
from datetime import datetime

# Ensure the 'data' directory exists
os.makedirs("data", exist_ok=True)

# Load latest league standings JSON dynamically
def load_latest_standings():
    files = sorted(
        [f for f in os.listdir("data/") if f.startswith("league_standings_") and f.endswith(".json")],
        key=lambda x: os.path.getctime(os.path.join("data/", x)),
        reverse=True
    )
    if files:
        latest_file = os.path.join("data/", files[0])
        with open(latest_file, "r") as f:
            return json.load(f)
    else:
        print("Error: League standings data not found.")
        return None

# Generate round-robin fixtures
def generate_fixtures(teams, gameweeks):
    fixtures = []
    matchups = list(itertools.combinations(teams, 2))  # All possible matchups
    
    for i, (home, away) in enumerate(matchups):
        gameweek = gameweeks[i % len(gameweeks)]  # Rotate through selected gameweeks
        fixtures.append({
            "Gameweek": gameweek,
            "Home": home,
            "Away": away
        })
    
    return fixtures

# Load standings and extract teams
standings = load_latest_standings()
if standings:
    teams = [team['Team Name'] for team in standings]
    
    # Define gameweeks for scheduling (Modify if needed)
    selected_gameweeks = [5, 7, 9, 11, 13, 15]  # Customizable
    
    # Generate fixtures
    fixtures = generate_fixtures(teams, selected_gameweeks)
    
    # Save fixtures to JSON
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    fixtures_filepath = f"data/fixtures_{timestamp}.json"
    with open(fixtures_filepath, "w") as f:
        json.dump(fixtures, f, indent=4)
    print(f"✅ Fixtures generated and saved to {fixtures_filepath}")
