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
    
    # Deep Dive & SQL Viewer
    with st.expander("📊 Analytical Deep Dive & Engineering Notes"):
        tab1, tab2 = st.tabs(["💡 Data Insights & Research", "⚙️ SQL & Optimization"])
        
        with tab1:
            st.markdown("""
            **Data Insights & Conclusions:**
            * **Wall Proximity is Punishing:** Street circuits (like Monaco or Baku) and old-school tracks (like Suzuka) dominate this list. Unlike modern circuits with vast asphalt run-off areas that forgive lock-ups, making a mistake on these tracks means immediate contact with a wall.
            * **The "First Lap" Factor:** Circuits with tight, heavy-braking first corners (like Monza's Turn 1) naturally generate higher collision rates purely due to the funneling effect on the opening lap.

            **Visualization Strategy:**
            * A **Horizontal Bar Chart** is standard practice for categorical data with long text labels (Circuit Names), ensuring no text overlap. The `Reds` color scale emphasizes severity.

            **Future Research Points:**
            * **Weather Correlation:** How many of these crashes occurred during wet conditions? Cross-referencing this with weather data could separate tracks that are inherently dangerous from tracks that just had a few chaotic, rainy weekends.
            """)
            
        with tab2:
            st.markdown("**The Engine Under the Hood:**")
            st.code(danger_query, language="sql")
            st.markdown("""
            **Query Optimization Insights:**
            * *Anti-Pattern Identification:* Hardcoding status strings (`IN ('Accident', 'Collision'...)`) inside the `WHERE` clause is a brittle practice. If the raw data introduces a new status like 'Crash', the query silently drops data.
            * *Data Architecture Fix:* Instead of filtering by text, the database should have a `dim_status` table where each `status_id` is categorized into broad buckets (e.g., `status_category = 'Crash'`). The query should then join and filter by the category, ensuring the logic remains robust and scalable.
            """)
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
    
    # Deep Dive & SQL Viewer
    with st.expander("📊 Analytical Deep Dive & Engineering Notes"):
        tab1, tab2 = st.tabs(["💡 Data Insights & Research", "⚙️ SQL & Optimization"])
        
        with tab1:
            st.markdown("""
            **Data Insights & Conclusions:**
            * **Car Breakers:** Some tracks are notorious for mechanical stress. For example, Monza requires the engine to be at 100% full throttle for most of the lap, leading to engine blowouts. Singapore's extreme heat and constant shifting destroy gearboxes and hydraulics.
            * **The Reliability Evolution:** If we filter this chart to only show post-2014 data, mechanical failures practically disappear compared to the early 2000s, showcasing the incredible leap in modern hybrid engine reliability.

            **Visualization Strategy:**
            * A **Grouped Bar Chart** perfectly contrasts the two metrics. The visual distinction allows us to quickly spot "anomalies"—tracks where mechanical failures actually outnumber driver errors.

            **Future Research Points:**
            * **Correlating Heat with Failures:** Cross-reference mechanical failures with historical ambient and track temperature data to prove the hypothesis that hotter races cause disproportionately more engine and hydraulic failures.
            """)
            
        with tab2:
            st.markdown("**The Engine Under the Hood:**")
            st.code(reliability_query, language="sql")
            st.markdown("""
            **Query Optimization Insights:**
            * *Data Transformation:* The SQL query utilizes **Conditional Aggregation** (`SUM(CASE WHEN...)`) to pivot row-level status data into distinct columns. We then use Pandas `pd.melt()` in Python to unpivot the data back into a long format required by Plotly for grouped bars.
            * *Compute Cost:* Executing multiple `IN (...)` string matching operations inside aggregate functions is CPU-heavy over millions of rows. 
            * *Data Engineering Fix:* The ETL pipeline should calculate boolean flags (e.g., `is_driver_error_dnf` = 1 or 0, `is_mechanical_dnf` = 1 or 0) directly during insertion. The query would then simply be `SUM(is_driver_error_dnf)`, turning a complex text-search into a lightning-fast integer summation.
            """)
else:
    st.warning("No data available for Reliability Analysis.")