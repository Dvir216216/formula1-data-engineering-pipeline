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
    
    # Deep Dive & SQL Viewer
    with st.expander("📊 Analytical Deep Dive & Engineering Notes"):
        tab1, tab2 = st.tabs(["💡 Data Insights & Research", "⚙️ SQL & Optimization"])
        
        with tab1:
            st.markdown("""
            **Data Insights & Conclusions:**
            * **Aerodynamics vs. Engine:** 'Technical' circuits (like Monaco or Singapore) reward high downforce and driver precision, while 'High Speed' circuits (Monza, Spa) favor raw engine power and low-drag setups.
            * **Driver Adaptability:** Drivers who show high win counts across *all three* track categories (Balanced, High Speed, Technical) demonstrate generational adaptability, proving their success is not purely reliant on a specific car characteristic.

            **Visualization Strategy:**
            * A **Grouped Bar Chart** effectively displays multi-dimensional categorical data. Grouping by 'Track Type' allows us to immediately spot which drivers dominate specific aerodynamic conditions compared to their peers.

            **Future Research Points:**
            * **Car vs. Driver Correlation:** Introduce constructor data to determine if a driver's dominance on 'High Speed' tracks was heavily inflated by driving a car with a superior engine (e.g., Mercedes PU from 2014-2016).
            * **Weather Adjustments:** Rain acts as a great equalizer. Analyzing wins in wet conditions on 'High Speed' tracks could isolate driver skill from pure machine performance.
            """)
            
        with tab2:
            st.markdown("**The Engine Under the Hood:**")
            st.code(track_type_query, language="sql")
            st.markdown("""
            **Query Optimization Insights:**
            * *Anti-Pattern Identification:* The query joins `track_types t` and `mv_race_complete_details v` on `circuit_name`. Joining on string (text) columns is computationally expensive and memory-inefficient compared to integer joins.
            * *Data Engineering Fix:* The track classification (`CASE` statement) evaluates per query execution. The ETL pipeline should pre-calculate the `avg_speed_kph` and assign a static `circuit_type_id` directly in the dimensional `circuits` table. The join should then strictly utilize integer keys (`circuitid`).
            """)
else:
    st.warning("No data available for Track Classification.")

st.divider()

# --- Section 2: Pole Position Kings ---
st.header("2. The Quali Masters (Pole Positions)")
st.markdown("Identifying drivers who dominated Saturday qualifying sessions across different circuits.")

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

    # Deep Dive & SQL Viewer
    with st.expander("📊 Analytical Deep Dive & Engineering Notes"):
        tab1, tab2 = st.tabs(["💡 Data Insights & Research", "⚙️ SQL & Optimization"])
        
        with tab1:
            st.markdown("""
            **Data Insights & Conclusions:**
            * **The One-Lap Pace Makers:** Qualifying (Saturday) requires extracting the absolute maximum grip from the tires over a single lap, which requires a completely different setup and driving style compared to race pace (Sunday).
            * **Circuit Specialists:** Seeing a driver hold the absolute record for pole positions at specific historic circuits highlights extreme synergy between a driver's specific driving style and the track's layout.

            **Visualization Strategy:**
            * A **Bubble Chart (Scatter with Size)** draws immediate attention to magnitude. The size of the bubble intuitively represents the scale of dominance (`pole_count`), allowing viewers to quickly scan for the highest all-time records across the grid.

            **Future Research Points:**
            * **Pole-to-Win Conversion Rate:** Does starting 1st actually guarantee a win? Analyzing the conversion rate of Pole Positions to Race Wins per circuit would reveal which tracks make overtaking nearly impossible (e.g., Monaco) versus tracks where slipstreaming favors the car starting 2nd (e.g., Mexico).
            """)
            
        with tab2:
            st.markdown("**The Engine Under the Hood:**")
            st.code(pole_query, language="sql")
            st.markdown("""
            **Query Optimization Insights:**
            * *Window Function Cost:* `DENSE_RANK() OVER (PARTITION BY...)` is a powerful analytical tool, but it forces the PostgreSQL engine to perform internal sorting operations which can be CPU-bound on large datasets.
            * *Materialization Strategy:* Since historical pole positions rarely change (only once a year per track), computing this ranking dynamically on every page load is inefficient. This result set is a prime candidate for a nightly aggregated table or a specialized Materialized View (e.g., `mv_driver_circuit_records`).
            """)
else:
    st.warning("No data available for Pole Positions.")