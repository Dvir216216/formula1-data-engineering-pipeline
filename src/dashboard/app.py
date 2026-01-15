import os
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
import plotly.express as px

# 1. Page Config
st.set_page_config(page_title="F1 Analytics Dashboard", page_icon="🏎️", layout="wide")

# 2. Database Connection
# Logic: Try to get DATABASE_URL from Docker environment; if not found, use localhost (for local testing without Docker)
DB_URI = os.getenv("DATABASE_URL", "postgresql://postgres:1234@localhost:5432/formula1")

@st.cache_data
def load_data(query):
    """Loads data from PostgreSQL using SQLAlchemy"""
    try:
        engine = create_engine(DB_URI)
        with engine.connect() as conn:
            df = pd.read_sql(text(query), conn)
        return df
    except Exception as e:
        st.error(f"Database Error: {e}")
        return pd.DataFrame()


# 3. Dashboard Header
st.title("🏎️ Formula 1 Analytics Platform")
st.markdown("### Powered by PostgreSQL (Materialized Views) & Python")

# --- Section 1: KPI Metrics ---
col1, col2, col3 = st.columns(3)

# Metric 1: Total Races
races_count = load_data("SELECT COUNT(*) FROM races").iloc[0, 0]
col1.metric("Total Races", races_count)

# Metric 2: Total Drivers
drivers_count = load_data("SELECT COUNT(*) FROM drivers").iloc[0, 0]
col2.metric("Total Drivers", drivers_count)

# Metric 3: Fastest Lap Ever
# NOTE: 'fastestlaptime' is not in the Materialized View, so we query the raw 'results' table.
try:
    # Casting to text to safely handle mixed formats
    lap_query = """
        SELECT MIN(fastestlaptime::text) 
        FROM results 
        WHERE fastestlaptime IS NOT NULL AND fastestlaptime != ''
    """
    fastest_lap = load_data(lap_query).iloc[0, 0]
    col3.metric("Record Lap Time", fastest_lap)
except:
    col3.metric("Record Lap Time", "N/A")

# --- Section 2: Visualization (Plotly) ---
st.divider()
st.subheader("🏆 Top 10 Drivers by Wins")

# Querying the Materialized View based on your SQL file
# We use 'positionorder = 1' for wins and 'driver_name' which exists in your MV.
query_wins = """
    SELECT 
        driver_name, 
        COUNT(*) as wins 
    FROM mv_race_complete_details 
    WHERE positionorder = 1 
    GROUP BY driver_name 
    ORDER BY wins DESC 
    LIMIT 10
"""
df_wins = load_data(query_wins)

if not df_wins.empty:
    # Plotly Bar Chart
    fig = px.bar(
        df_wins,
        x='driver_name',
        y='wins',
        color='wins',
        color_continuous_scale='Viridis',
        text='wins',
        labels={'driver_name': 'Driver', 'wins': 'Wins'},
        title='Most Successful Drivers (All Time)'
    )

    # Sorting and Layout
    fig.update_layout(
        xaxis_title="Driver",
        yaxis_title="Total Wins",
        xaxis={'categoryorder': 'total descending'},  # Forces correct sorting
        coloraxis_showscale=False
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("No data found in Materialized View. Please run the SQL script.")

# --- Section 3: Raw Data Explorer ---
with st.expander("🔍 View Raw Data (Recent Years)"):
    # Sorted by 'year' because 'date' is not in your Materialized View
    df_raw = load_data("SELECT * FROM mv_race_complete_details ORDER BY year DESC LIMIT 100")
    st.dataframe(df_raw)