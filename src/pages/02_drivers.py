import streamlit as st
import plotly.express as px

# --- Page Configuration ---
st.set_page_config(page_title="Track Mastery", layout="wide")

# --- Load Data Function ---
load_data = st.session_state.get('load_data')
if not load_data:
    st.error("🚨 Please start the app from the Main Page (app.py)")
    st.stop()

# --- Page Header ---
st.title("🏆 Track Mastery & Driver Profiles")
st.markdown("""
Explore how different drivers adapt to various track conditions and discover 
the all-time masters of qualifying (Pole Positions).
""")
st.divider()

# --- Section 1: Track Classification & Driver Success ---
st.header("1. Driver Success by Track Type")
st.markdown("Classifying circuits based on average speed to identify where specific drivers excel.")

# Defined the query using 'driverref' instead of the non-existent 'driver_name'
track_type_query = """
WITH track_stats AS (
    SELECT 
        circuit_name,
        AVG(CAST(fastestlapspeed AS NUMERIC)) AS avg_speed_kph
    FROM mv_race_complete_details
    WHERE year >= 2014 AND fastestlapspeed IS NOT NULL
    GROUP BY circuit_name
),
track_types AS (
    SELECT 
        circuit_name,
        CASE
            WHEN avg_speed_kph > 210 THEN 'High Speed'
            WHEN avg_speed_kph < 180 THEN 'Technical'
            ELSE 'Balanced'
        END AS circuit_type
    FROM track_stats
)
SELECT 
    t.circuit_type,
    v.driverref AS driver_name,
    COUNT(*) AS wins
FROM track_types t
JOIN mv_race_complete_details v ON t.circuit_name = v.circuit_name
WHERE v.positionorder = 1 AND v.year >= 2014
GROUP BY t.circuit_type, v.driverref
HAVING COUNT(*) >= 3
ORDER BY wins DESC;
"""

df_tracks = load_data(track_type_query)

if not df_tracks.empty:
    fig_tracks = px.bar(
        df_tracks, 
        x="circuit_type", 
        y="wins", 
        color="driver_name",
        title="Wins by Track Characteristics (Hybrid Era)",
        labels={"circuit_type": "Track Type", "wins": "Total Wins", "driver_name": "Driver"},
        barmode="group"
    )
    st.plotly_chart(fig_tracks, use_container_width=True)
    
    # SQL Viewer
    with st.expander("🔍 View the SQL Engine (Track Classification)"):
        st.markdown("This query calculates the average speed per track to classify it, then joins the results to find the most successful drivers per category.")
        st.code(track_type_query, language="sql")
else:
    st.warning("No data available for Track Classification.")

st.divider()

# --- Section 2: Pole Position Kings ---
st.header("2. The Quali Masters (Pole Positions)")
st.markdown("Identifying drivers who dominated Saturday qualifying sessions across different circuits.")

# Refactored to use 'driverref'
pole_query = """
WITH PolePositionData AS (
    SELECT 
        circuit_name, 
        driverref AS driver_name, 
        COUNT(*) as pole_count,
        DENSE_RANK() OVER (PARTITION BY circuit_name ORDER BY COUNT(*) DESC) as rank_in_circuit
    FROM mv_race_complete_details
    WHERE grid = 1
    GROUP BY circuit_name, driverref
)
SELECT 
    circuit_name, 
    driver_name, 
    pole_count
FROM PolePositionData
WHERE rank_in_circuit = 1 AND pole_count >= 3
ORDER BY pole_count DESC
LIMIT 15;
"""

df_pole = load_data(pole_query)

if not df_pole.empty:
    fig_pole = px.scatter(
        df_pole, 
        x="circuit_name", 
        y="pole_count", 
        color="driver_name",
        size="pole_count",
        title="Track-Specific Pole Position Records",
        labels={"circuit_name": "Circuit", "pole_count": "Pole Positions", "driver_name": "Driver"}
    )
    fig_pole.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig_pole, use_container_width=True)

    # SQL Viewer
    with st.expander("🔍 View the SQL Engine (Window Functions)"):
        st.markdown("This query uses `DENSE_RANK() OVER (PARTITION BY...)` to find the top qualifier for each distinct circuit.")
        st.code(pole_query, language="sql")
else:
    st.warning("No data available for Pole Positions.")