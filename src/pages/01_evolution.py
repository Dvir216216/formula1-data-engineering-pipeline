import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# --- Page Configuration ---
st.set_page_config(page_title="Evolution of Speed", layout="wide")

# --- Load Data Function ---
load_data = st.session_state.get('load_data')
if not load_data:
    st.error("🚨 Please start the app from the Main Page (app.py)")
    st.stop()

# --- Page Header ---
st.title("⏱️ The Evolution of Speed & Technology")
st.markdown("""
Analyze how car performance has improved over the decades, highlighting the historic 
Monaco circuit and the dominance of specific constructors in the Hybrid Era (2014-Present).
""")
st.divider()

# --- Section 1: Monaco Lap Time Evolution ---
st.header("1. Monaco Circuit: 20 Years of Performance")
st.info("💡 Data Insight: Notice the significant drop in lap times around 2017 due to new aerodynamic regulations introducing wider, faster cars.")

monaco_query = """
WITH yearly_stats AS (
    SELECT 
        year,
        MIN(CAST(fastestlaptime AS INTERVAL)) AS best_race_lap,
        AVG(CAST(fastestlaptime AS INTERVAL)) AS avg_lap_time
    FROM mv_race_complete_details
    WHERE circuit_name = 'Circuit de Monaco'
      AND fastestlaptime IS NOT NULL
      AND year >= 2004
    GROUP BY year
)
SELECT 
    year,
    EXTRACT(EPOCH FROM best_race_lap) as best_lap_seconds,
    EXTRACT(EPOCH FROM avg_lap_time) as avg_lap_seconds
FROM yearly_stats
ORDER BY year;
"""

df_monaco = load_data(monaco_query)

if not df_monaco.empty:
    fig_monaco = go.Figure()
    fig_monaco.add_trace(go.Scatter(x=df_monaco['year'], y=df_monaco['best_lap_seconds'],
                                    mode='lines+markers', name='Best Lap (Seconds)'))
    fig_monaco.add_trace(go.Scatter(x=df_monaco['year'], y=df_monaco['avg_lap_seconds'],
                                    mode='lines', name='Field Average', line=dict(dash='dash')))
    
    fig_monaco.update_layout(title="Monaco Lap Time Progression (2004-Present)",
                             xaxis_title="Year", yaxis_title="Time in Seconds")
    st.plotly_chart(fig_monaco, use_container_width=True)
    
    # Deep Dive & SQL Viewer
    with st.expander("📊 Analytical Deep Dive & Engineering Notes"):
        tab1, tab2 = st.tabs(["💡 Data Insights & Research", "⚙️ SQL & Optimization"])
        
        with tab1:
            st.markdown("""
            **Data Insights & Conclusions:**
            * **Regulation Over Engineering:** The general trend shows car speed is largely dictated by FIA regulations. The massive drop in lap times around 2017 aligns with the introduction of wider cars and significantly higher downforce rules.
            * **Spikes in the Data:** Occasional severe spikes (slower times) often correlate with wet-weather races, pulling the field average significantly higher.

            **Visualization Strategy:**
            * A dual-trace **Line Chart** is optimal for time-series data. Plotting both the absolute limit (Best Lap) and the field average demonstrates not just the peak engineering capability, but the overall competitiveness of the grid.

            **Future Research Points:**
            * **Weather API Integration:** Filter out wet sessions to compare purely dry pace.
            * **Regulation Mapping:** Overlay vertical lines on the chart representing major rule changes (e.g., 2014 V6 Hybrid, 2022 Ground Effect) to measure the immediate impact of regulatory shifts.
            """)
            
        with tab2:
            st.markdown("**The Engine Under the Hood:**")
            st.code(monaco_query, language="sql")
            st.markdown("""
            **Query Optimization Insights:**
            * By utilizing the `mv_race_complete_details` Materialized View, we bypassed the heavy joins required to link circuits, races, and results.
            * *Refactoring Opportunity:* Casting `fastestlaptime` to `INTERVAL` on the fly is CPU-intensive. A better architectural approach is to parse string lap times into integer milliseconds during the Python ETL pipeline before pushing to PostgreSQL.
            """)
else:
    st.warning("No data available for Monaco Lap Times.")

st.divider()

# --- Section 2: Constructor Dominance (Hybrid Era) ---
st.header("2. Constructor Dominance in the Hybrid Era")
st.markdown("Which team has maintained the highest average pace since the introduction of hybrid engines in 2014?")

constructor_query = """
SELECT 
    constructor_name,
    AVG(EXTRACT(EPOCH FROM CAST('00:' || fastestlaptime AS INTERVAL))) AS avg_pace
FROM mv_race_complete_details
WHERE year >= 2014 AND fastestlaptime IS NOT NULL
GROUP BY constructor_name
ORDER BY avg_pace ASC
LIMIT 10;
"""

df_cons = load_data(constructor_query)

if not df_cons.empty:
    fig_cons = px.bar(df_cons, x='avg_pace', y='constructor_name', orientation='h',
                      title="Top 10 Fastest Teams (Hybrid Era Average Pace)",
                      labels={'avg_pace': 'Avg Lap Pace (Seconds)', 'constructor_name': 'Team'},
                      color='avg_pace', color_continuous_scale='Reds_r')
    
    fig_cons.update_layout(yaxis={'categoryorder':'total descending'})
    st.plotly_chart(fig_cons, use_container_width=True)
    
    # Deep Dive & SQL Viewer
    with st.expander("📊 Analytical Deep Dive & Engineering Notes"):
        tab1, tab2 = st.tabs(["💡 Data Insights & Research", "⚙️ SQL & Optimization"])
        
        with tab1:
            st.markdown("""
            **Data Insights & Conclusions:**
            * **The Early Adopter Advantage:** Teams that nailed the complex V6 Turbo-Hybrid regulations early (e.g., Mercedes) established a multi-year dominance. 
            * **Pace Discrepancy:** The gap between the top tier and the midfield becomes glaringly obvious when aggregated over multiple seasons, highlighting the correlation between team budgets and engineering output.

            **Visualization Strategy:**
            * A **Horizontal Bar Chart** provides immediate readability for categorical data (Teams). Sorting descending forces the fastest teams to the top. The `Reds_r` color scale subconsciously associates lower (faster) times with high performance.

            **Future Research Points:**
            * **Consistency vs. Peak Pace:** Calculate the Standard Deviation (`STDDEV`) of lap times. A team might have a fast average but high volatility due to unreliability.
            * **Time-Series Breakdown:** Track how the gap between the #1 constructor and the rest of the field has narrowed or widened year over year.
            """)
            
        with tab2:
            st.markdown("**The Engine Under the Hood:**")
            st.code(constructor_query, language="sql")
            st.markdown("""
            **Query Optimization Insights:**
            * *The String Manipulation Bottleneck:* The operation `CAST('00:' || fastestlaptime AS INTERVAL)` forces the PostgreSQL engine to do string concatenation and data type casting for every single row matching the `WHERE` clause. 
            * *Data Engineering Fix:* This violates the principle of "Compute Once, Read Many". The ETL pipeline should be updated to compute `lap_time_ms` as a native integer column directly in the `results` table to drastically reduce query execution cost.
            """)
else:
    st.warning("No data available for Constructor analysis.")