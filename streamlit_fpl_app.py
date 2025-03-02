import requests
import pandas as pd
import json
import os
from datetime import datetime
import sys

# Fixture Scheduling Script

# Load league ID from config file
CONFIG_FILE = "data/config.json"
if os.path.exists(CONFIG_FILE):
    with open(CONFIG_FILE, "r") as f:
        config = json.load(f)
    LEAGUE_ID = config.get("league_id", "857")
else:
    LEAGUE_ID = "857"  # Default league ID if no config file is found

# API endpoints
LEAGUE_API_URL = f"https://fantasy.premierleague.com/api/leagues-classic/{LEAGUE_ID}/standings/"

# Ensure the 'data' directory exists
os.makedirs("data", exist_ok=True)

# Fetch league standings
def fetch_league_standings():
    response = requests.get(LEAGUE_API_URL)
    
    if response.status_code == 200:
        data = response.json()
        teams = []
        
        for entry in data['standings']['results']:
            teams.append({
                'Rank': entry['rank'],
                'Team Name': entry['entry_name'],
                'Manager': entry['player_name'],
                'Total Points': entry['total'],
                'FPL Team ID': entry['entry']  # Needed for individual stats
            })
        
        df = pd.DataFrame(teams)
        return df
    else:
        print("Error fetching league standings:", response.status_code)
        return None

# Save data to JSON
def save_to_json(data, filename):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filepath = f"data/{filename}_{timestamp}.json"
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=4)
    print(f"Saved data to {filepath}")

# Run functions
league_standings_df = fetch_league_standings()
if league_standings_df is not None:
    print(league_standings_df.head())
    save_to_json(league_standings_df.to_dict(orient='records'), "league_standings")
