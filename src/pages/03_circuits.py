import streamlit as st
import plotly.express as px
import pandas as pd

# --- Page Configuration ---
st.set_page_config(page_title="Circuit Risk & Stats", layout="wide")

# --- Load Data Function ---
load_data = st.session_state.get('load_data')
if not load_data:
    st.error("🚨 Please start the app from the Main Page (app.py)")
    st.stop()

# --- Page Header ---
st.title("🏁 Circuit Risk & Reliability Statistics")
st.markdown("""
Analyze the historical danger levels of F1 circuits. Which tracks forgive mistakes, 
and which ones are known as 'car breakers' due to high crash rates or mechanical stress?
""")
st.divider()

# --- Section 1: The Danger Zone (Most Accidents) ---
st.header("1. The Danger Zone: Most Accidents")
st.markdown("Circuits ranked by the total number of crashes and collisions (2000 - Present).")

# Define the query: Filtering by specific crash-related status strings
danger_query = """
SELECT 
    circuit_name,
    COUNT(*) AS total_crashes
FROM mv_race_complete_details
WHERE year >= 2000 
  AND status_text IN ('Accident', 'Collision', 'Spun off', 'Collision damage')
GROUP BY circuit_name
ORDER BY total_crashes DESC
LIMIT 15;
"""

df_danger = load_data(danger_query)

if not df_danger.empty:
    fig_danger = px.bar(
        df_danger, 
        x="total_crashes", 
        y="circuit_name", 
        orientation="h",
        title="Top 15 Most Dangerous Circuits (By Total Crashes)",
        labels={"total_crashes": "Total Crashes & Collisions", "circuit_name": "Circuit"},
        color="total_crashes", 
        color_continuous_scale="Reds"
    )
    fig_danger.update_layout(yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig_danger, use_container_width=True)
    
    # SQL Viewer
    with st.expander("🔍 View the SQL Engine (Accident Filtering)"):
        st.markdown("This query filters the `status_text` for crash-related keywords to aggregate total incidents per track.")
        st.code(danger_query, language="sql")
else:
    st.warning("No data available for Danger Zone.")

st.divider()

# --- Section 2: Crashes vs Mechanical Failures ---
st.header("2. Track Reliability: Driver Error vs. Machine Failure")
st.markdown("Comparing tracks that cause driver mistakes (Crashes) versus tracks that destroy cars (Mechanical Failures).")

# Define the query: Using CASE WHEN to pivot DNF reasons
reliability_query = """
SELECT 
    circuit_name,
    SUM(CASE WHEN status_text IN ('Accident', 'Collision', 'Spun off', 'Collision damage') THEN 1 ELSE 0 END) AS driver_errors,
    SUM(CASE WHEN status_text IN ('Engine', 'Gearbox', 'Hydraulics', 'Suspension', 'Brakes', 'Electrical') THEN 1 ELSE 0 END) AS mechanical_failures
FROM mv_race_complete_details
WHERE year >= 2000
GROUP BY circuit_name
HAVING SUM(CASE WHEN status_text IN ('Accident', 'Collision') THEN 1 ELSE 0 END) > 10
ORDER BY driver_errors DESC
LIMIT 10;
"""

df_reliability = load_data(reliability_query)

if not df_reliability.empty:
    # Melt the dataframe for Plotly grouped bar chart (converting columns to rows)
    df_melted = pd.melt(
        df_reliability, 
        id_vars=['circuit_name'], 
        value_vars=['driver_errors', 'mechanical_failures'],
        var_name='failure_type', 
        value_name='incident_count'
    )
    
    # Clean up labels for a polished display
    df_melted['failure_type'] = df_melted['failure_type'].str.replace('_', ' ').str.title()
    
    fig_reliability = px.bar(
        df_melted, 
        x="circuit_name", 
        y="incident_count", 
        color="failure_type",
        title="Driver Errors vs Mechanical Failures (Top 10 Tracks)",
        labels={"circuit_name": "Circuit", "incident_count": "Number of Incidents", "failure_type": "Incident Type"},
        barmode="group",
        color_discrete_map={"Driver Errors": "#ef553b", "Mechanical Failures": "#636efa"}
    )
    fig_reliability.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig_reliability, use_container_width=True)
    
    # SQL Viewer
    with st.expander("🔍 View the SQL Engine (Conditional Aggregation)"):
        st.markdown("This query uses `SUM(CASE WHEN...)` to pivot the reasons for Did Not Finish (DNF) into distinct columns for comparison.")
        st.code(reliability_query, language="sql")
else:
    st.warning("No data available for Reliability Analysis.")