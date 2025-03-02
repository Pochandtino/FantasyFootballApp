import requests
import pandas as pd
import json
import os
from datetime import datetime

# Fetch FPL Data Script

# Define the league ID
LEAGUE_ID = 857  # Update if needed

# API endpoints
LEAGUE_API_URL = f"https://fantasy.premierleague.com/api/leagues-classic/{LEAGUE_ID}/standings/"
TEAM_API_URL = "https://fantasy.premierleague.com/api/entry/{}/history/"

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

# Fetch individual team stats
def fetch_team_stats(team_id):
    response = requests.get(TEAM_API_URL.format(team_id))
    
    if response.status_code == 200:
        data = response.json()
        history = data.get('current', [])
        past_seasons = data.get('past', [])
        
        total_points = past_seasons[-1]['total_points'] if past_seasons else (history[-1]['total_points'] if history else 0)
        
        team_data = {
            'Team ID': team_id,
            'Total Points': total_points,
            'Gameweek Points': [gw['points'] for gw in history] if history else [],
            'Transfers': [gw['event_transfers'] for gw in history] if history else [],
            'Chips Used': [gw['chips'] if 'chips' in gw else None for gw in history]
        }
        return team_data
    else:
        print(f"Error fetching data for team {team_id}:", response.status_code)
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
    
    # Fetch stats for all teams
    team_stats_list = []
    for team_id in league_standings_df['FPL Team ID']:
        team_stats = fetch_team_stats(team_id)
        if team_stats:
            team_stats_list.append(team_stats)
    
    # Convert to DataFrame
    team_stats_df = pd.DataFrame(team_stats_list)
    print(team_stats_df.head())
    save_to_json(team_stats_df.to_dict(orient='records'), "team_stats")
