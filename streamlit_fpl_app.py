import streamlit as st
import pandas as pd
import json
import os

# Load JSON data
DATA_PATH = "data/"

def load_json(filename):
    filepath = os.path.join(DATA_PATH, filename)
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            return json.load(f)
    return None

# Load data files
league_standings = load_json("league_standings_latest.json")
fixtures = load_json("fixtures.json")

# Streamlit UI
st.title("🏆 Fantasy Premier League Tournament")

# Display League Standings
st.header("📊 League Standings")
if league_standings:
    df_standings = pd.DataFrame(league_standings)
    st.dataframe(df_standings)
else:
    st.warning("League standings data not found.")

# Display Fixtures
st.header("📅 Fixture Schedule")
if fixtures:
    df_fixtures = pd.DataFrame(fixtures)
    gameweek_filter = st.selectbox("Select Gameweek:", sorted(df_fixtures["Gameweek"].unique()))
    filtered_fixtures = df_fixtures[df_fixtures["Gameweek"] == gameweek_filter]
    st.dataframe(filtered_fixtures)
else:
    st.warning("Fixture data not found.")

# Custom Gameweek Selection for Fixtures
st.header("⚙️ Customize Fixture Gameweeks")
default_gameweeks = [5, 7, 9, 11, 13, 15]
selected_gameweeks = st.multiselect("Select gameweeks for fixture scheduling:", list(range(1, 39)), default=default_gameweeks)
if st.button("Update Fixtures"):
    st.success(f"Fixtures will be generated using gameweeks: {selected_gameweeks}")
    # Future: Save this selection & regenerate fixtures
