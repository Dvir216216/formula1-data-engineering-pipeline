import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
import os

# --- 1. Page Configuration ---
st.set_page_config(page_title="F1 Analytics Platform", page_icon="🏎️", layout="wide")

# --- 2. Database Connection Management ---
@st.cache_resource
def init_connection():
    db_url = st.secrets.get("DATABASE_URL") or os.getenv("DATABASE_URL")
    if not db_url:
        st.error("🚨 DATABASE_URL is missing! Please configure secrets.")
        st.stop()
    engine = create_engine(db_url)
    return engine

# --- 3. Data Loading Function ---
@st.cache_data(ttl=43200, show_spinner="Fetching data from Neon...")
def load_data(query: str):
    engine = init_connection()
    try:
        with engine.connect() as conn:
            df = pd.read_sql(text(query), conn)
        return df
    except Exception as e:
        st.error(f"Database Query Error: {e}")
        return pd.DataFrame()

st.session_state['load_data'] = load_data

# --- 4. Navigation (Multi-Page Router) ---
pages = {
    "Dashboards": [
        st.Page("pages/01_evolution.py", title="Evolution of Speed", icon="⏱️"),
        st.Page("pages/02_drivers.py", title="Track Mastery", icon="🏆"),
        st.Page("pages/03_circuits.py", title="Circuit Risk & Stats", icon="🏁"), # הוספנו את העמוד השלישי
    ]
}

pg = st.navigation(pages)
pg.run()