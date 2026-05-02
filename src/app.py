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
    
    # תיקון 1: הוספת pool_pre_ping=True - זהו ה"דופק" שבודק אם החיבור חי לפני השימוש
    # תיקון 2: הוספת pool_recycle=300 - מרענן חיבורים כל 5 דקות כדי למנוע מהם להתיישן
    engine = create_engine(
        db_url, 
        pool_pre_ping=True, 
        pool_recycle=300,
        connect_args={"sslmode": "require"} # מבטיח חיבור SSL מאובטח ותקין
    )
    return engine

# --- 3. Data Loading Function ---
# תיקון 3: הורדת ה-TTL לערך סביר יותר (למשל שעה) וטיפול נכון בשגיאות
@st.cache_data(ttl=3600, show_spinner="Fetching data from Neon...")
def load_data(query: str):
    engine = init_connection()
    try:
        with engine.connect() as conn:
            df = pd.read_sql(text(query), conn)
        return df
    except Exception as e:
        # אם יש שגיאה, אנחנו לא רוצים לשמור אותה בקאש, אז ננקה אותו לאותה שאילתה
        st.cache_data.clear()
        st.error(f"Database Query Error: {e}")
        return pd.DataFrame()

st.session_state['load_data'] = load_data

# --- 4. Navigation (Multi-Page Router) ---
pages = {
    "Overview": [
        st.Page("pages/00_home.py", title="Home", icon="🏠"),
    ],
    "Dashboards": [
        st.Page("pages/01_evolution.py", title="Evolution of Speed", icon="⏱️"),
        st.Page("pages/02_drivers.py", title="Track Mastery", icon="🏆"),
        st.Page("pages/03_circuits.py", title="Circuit Risk & Stats", icon="🏁"), 
        st.Page("pages/04_optimization.py", title="Performance Metrics", icon="⚡"),
    ]
}

pg = st.navigation(pages)
pg.run()