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
    
    # SQL Viewer
    with st.expander("🔍 View the SQL Engine (Lap Time Evolution)"):
        st.markdown("This query extracts the fastest single lap and the average field lap time per year, converting PostgreSQL `INTERVAL` types into seconds (`EPOCH`) for accurate plotting.")
        st.code(monaco_query, language="sql")
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
    
    # SQL Viewer
    with st.expander("🔍 View the SQL Engine (Constructor Pace)"):
        st.markdown("This query calculates the average lap pace across all tracks for each constructor, limiting the results to the top 10 fastest teams.")
        st.code(constructor_query, language="sql")
else:
    st.warning("No data available for Constructor analysis.")