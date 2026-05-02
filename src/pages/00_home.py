import streamlit as st

st.set_page_config(page_title="F1 Data Platform", layout="wide", initial_sidebar_state="expanded")

st.title("🏎️ Formula 1 Data Engineering Platform")
st.markdown("### End-to-End Data Architecture & Analytics Pipeline")
st.divider()

st.markdown("""
Welcome to the Formula 1 Data Engineering Portfolio Project. 
This platform demonstrates a complete data lifecycle: from extracting raw CSV files, designing a relational PostgreSQL database schema, performing analytical queries, to optimizing disk I/O and computing costs.
""")

st.header("📂 Project Modules")

col1, col2 = st.columns(2)

with col1:
    st.info("""
    **⏱️ Evolution of Speed (ETL & History)**
    Explores the historical progression of F1. Showcases basic data extraction, transformation, and load (ETL) processes, mapping out how the sport has evolved over the decades.
    """)
    
    st.success("""
    **🏁 Circuit Risk & Stats**
    A deep dive into track data. Analyzes safety metrics, average speeds, and the characteristics of different circuits around the world using complex aggregations.
    """)

with col2:
    st.warning("""
    **🏆 Track Mastery (Drivers)**
    Focuses on driver performance analytics. Utilizes SQL window functions and complex joins to rank drivers, compare historical dominance, and extract meaningful business logic.
    """)
    
    st.error("""
    **⚡ Performance Metrics (Database Optimization)**
    *The core Data Engineering module.* Demonstrates real-world ROI by tackling database bottlenecks. Compares Execution Time and Query Cost before and after applying Materialized Views and Clustered Indexing.
    """)

st.divider()
st.markdown("""
*Built with: PostgreSQL, Python, Pandas, Plotly, and Streamlit.*  
*Deployed directly from Git using Streamlit Cloud.*
""")