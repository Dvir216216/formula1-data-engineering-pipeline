import streamlit as st

# הגדרת עמוד - הפעם נשאיר את הסרגל פתוח (expanded) כדי שיהיה ברור
st.set_page_config(page_title="F1 Data Platform", layout="wide", initial_sidebar_state="expanded")

# --- Navigation Hint ---
# חלונית בולטת עם חץ שמפנה לסרגל הצידי
st.info("↖️ **Use the sidebar on the left to explore different modules!**")

st.title("🏎️ Formula 1 Data Engineering Platform")
st.markdown("### End-to-End Data Architecture & Analytics Pipeline")
st.divider()

st.markdown("""
Welcome to the Formula 1 Data Engineering Portfolio Project. 
This platform demonstrates a complete data lifecycle: from extracting raw CSV files[cite: 1], 
designing a relational PostgreSQL database schema[cite: 2], performing analytical queries[cite: 3], 
to optimizing disk I/O and computing costs.
""")

st.header("📂 Project Modules")

col1, col2 = st.columns(2)

with col1:
    st.info("""
    **⏱️ Evolution of Speed (ETL & History)**
    Explores the historical progression of F1. Showcases basic data extraction, transformation, and load (ETL) processes[cite: 1].
    """)
    
    st.success("""
    **🏁 Circuit Risk & Stats**
    A deep dive into track data. Analyzes safety metrics and the characteristics of different circuits[cite: 3].
    """)

with col2:
    st.warning("""
    **🏆 Track Mastery (Drivers)**
    Focuses on driver performance analytics. Utilizes SQL window functions to rank drivers and compare historical dominance[cite: 2].
    """)
    
    st.error("""
    **⚡ Performance Metrics (Database Optimization)**
    *The core Data Engineering module.* Demonstrates real-world ROI by tackling database bottlenecks using Materialized Views and Indexing.
    """)

st.divider()
st.markdown("""
*Built with: PostgreSQL, Python, Pandas, Plotly, and Streamlit.*  
*Deployed directly from Git using Streamlit Cloud.*
""")