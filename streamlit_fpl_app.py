import streamlit as st
import pandas as pd
import json
import os
import glob

# Load latest JSON file dynamically
DATA_PATH = "data/"

def get_latest_json(filename_prefix):
    files = glob.glob(os.path.join(DATA_PATH, f"{filename_prefix}_*.json"))
    if files:
        latest_file = max(files, key=os.path.getctime)  # Get the newest file
        with open(latest_file, "r") as f:
            return json.load(f)
    return None

# Load data files
league_standings = get_latest_json("league_standings")
team_stats = get_latest_json("team_stats")
fixtures = get_latest_json("fixtures")

# Streamlit UI
st.set_page_config(page_title="Fantasy Premier League", layout="wide")
st.title("🏆 Fantasy Premier League Tournament")

# Display League Standings
st.header("📊 League Standings")
if league_standings:
    df_standings = pd.DataFrame(league_standings)
    df_standings = df_standings.sort_values(by=["Total Points"], ascending=False)  # Default sorting
    st.dataframe(df_standings.style.format({"Total Points": "{:,}"}))
else:
    st.warning("League standings data not found.")

# Display Team Stats
st.header("📈 Team Stats")
if team_stats:
    df_team_stats = pd.DataFrame(team_stats)
    st.dataframe(df_team_stats.style.format({"Total Points": "{:,}"}))
else:
    st.warning("Team stats data not found.")

# Display Fixtures
st.header("📅 Fixture Schedule")
if fixtures:
    df_fixtures = pd.DataFrame(fixtures)
    gameweek_filter = st.selectbox("Select Gameweek:", sorted(df_fixtures["Gameweek"].unique()), index=0)
    filtered_fixtures = df_fixtures[df_fixtures["Gameweek"] == gameweek_filter]
    st.dataframe(filtered_fixtures)
else:
    st.warning("Fixture data not found. Ensure the fixture generator is running.")

# Custom Gameweek Selection for Fixtures
st.header("⚙️ Customize Fixture Gameweeks")
default_gameweeks = [5, 7, 9, 11, 13, 15]
selected_gameweeks = st.multiselect("Select gameweeks for fixture scheduling:", list(range(1, 39)), default=default_gameweeks)
if st.button("Update Fixtures"):
    if selected_gameweeks:
        st.success(f"Fixtures will be generated using gameweeks: {selected_gameweeks}")
    else:
        st.error("Please select at least one gameweek.")
