import streamlit as st
import os
import pandas as pd
import plotly.graph_objects as go

# --- Page Config ---
st.set_page_config(page_title="Performance Optimization", layout="wide")

st.title("⚡ Performance Optimization & Benchmarks")
st.markdown("Measuring the impact of Data Engineering practices (Materialized Views & Indexing) on query latency and compute cost.")
st.divider()

# --- Section 1: Materialized Views ---
st.header("1. Defeating the 'Join Overhead' with Materialized Views")
st.markdown("Standard queries require PostgreSQL to join 5 heavy tables in real-time. By pre-computing the data into a physical Materialized View, we bypassed the massive CPU overhead.")

try:
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    csv_path = os.path.join(BASE_DIR, 'data', 'benchmarks', 'benchmark_results.csv')
    df_mv = pd.read_csv(csv_path)

    # 1. Extract KPI values for the extreme cases (Case 1 vs Case 5)
    baseline_df = df_mv[df_mv['scenario'].str.contains('Case 1', na=False, case=False)]
    mv_df = df_mv[df_mv['scenario'].str.contains('Case 5', na=False, case=False)]

    if not baseline_df.empty and not mv_df.empty:
        baseline_time = baseline_df['execution_time_ms'].values[0]
        mv_time = mv_df['execution_time_ms'].values[0]
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Baseline Execution Time", f"{baseline_time} ms")
        improvement = round((baseline_time - mv_time) / baseline_time * 100, 2)
        col2.metric("Optimized Execution Time", f"{mv_time} ms", f"-{improvement}% Latency", delta_color="inverse")

    # 2. Render Chart with ALL 5 CASES
    fig = go.Figure()
    fig.add_trace(go.Bar(x=df_mv['scenario'], y=df_mv['execution_time_ms'], name="Execution Time (ms)", marker_color='#ef553b'))
    fig.add_trace(go.Scatter(x=df_mv['scenario'], y=df_mv['cost_estimate'], name="Query Cost (I/O & CPU)", mode='lines+markers',
                             line=dict(color='#636efa', width=3), marker=dict(size=8), yaxis='y2'))

    fig.update_layout(
        title="Full Optimization Path: From Raw SQL to Materialized View",
        yaxis=dict(title="Execution Time (ms)", range=[0, 5]),
        yaxis2=dict(title="Cost Estimate", overlaying='y', side='right', rangemode='tozero'),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig, use_container_width=True)

    # --- Section 1: Decision Matrix ---
    st.subheader("⚖️ Architecture Decision Matrix: View vs. Materialized View")
    
    mv_logic = {
        "Feature": ["Data Freshness", "Query Speed", "Update Mechanism", "Storage cost", "When to use?"],
        "Standard View": ["Real-Time (Live)", "Slow (Runs joins every time)", "None (Virtual)", "None", "Simple logic / Security / Rare access"],
        "Materialized View": ["Snapshot (Delayed)", "Ultra-Fast (Physical table)", "Manual / Scheduled Refresh", "Physical Storage used", "High-traffic dashboards / Complex joins"]
    }
    st.table(pd.DataFrame(mv_logic))

    st.info("""
    🔄 **Trigger Strategy:** To bridge the gap in data freshness, you can add a **Database Trigger** on the base tables that executes 
    `REFRESH MATERIALIZED VIEW` after every `INSERT`. **Caution:** Only do this for low-write tables, as triggers add latency to every write operation.
    """)

    with st.expander("🔍 View All 5 SQL Scenarios"):
        st.code("""
-- Case 1: Raw SQL (Baseline)
-- Case 2: Standard View (Logical abstraction, no speed gain)
-- Case 3: Standard View + Index (Slight gain from faster filters)
-- Case 4: Materialized View (No Index) - Eliminates Joins but slow filtering
-- Case 5: Materialized View + Index - The Ultimate Performance Profile
        """, language="sql")
        st.dataframe(df_mv, use_container_width=True)

except Exception as e:
    st.error(f"🚨 Section 1 Error: {e}")


# --- Section 2: Clustered Indexing ---
st.divider()
st.header("2. Optimizing Disk I/O: Clustered Indexing")
st.markdown("Evaluating how physical data arrangement on disk impacts 'Random' vs 'Sequential' reads.")

try:
    idx_csv_path = os.path.join(BASE_DIR, 'data', 'benchmarks', 'benchmark_indexes.csv')
    df_idx = pd.read_csv(idx_csv_path)
    df_lap = df_idx[df_idx['query_name'] == 'Lap Times Search']

    fig2 = go.Figure()
    fig2.add_trace(go.Bar(x=df_lap['scan_type'], y=df_lap['execution_time_ms'], name="Execution Time (ms)", marker_color='#ef553b'))
    fig2.add_trace(go.Scatter(x=df_lap['scan_type'], y=df_lap['cost_estimate'], name="Query Cost (Pages Read)", mode='lines+markers',
                             line=dict(color='#636efa', width=3), marker=dict(size=8), yaxis='y2'))

    fig2.update_layout(title="Disk I/O Optimization: The Impact of Physical Sorting",
                      yaxis=dict(title="Execution Time (ms)", rangemode='tozero'),
                      yaxis2=dict(title="Cost Estimate", overlaying='y', side='right', rangemode='tozero'))
    st.plotly_chart(fig2, use_container_width=True)

    # --- Section 2: Decision Matrix ---
    st.subheader("⚖️ Strategy Guide: When to Cluster?")
    
    cluster_logic = {
        "Metric": ["Primary Key / ID Lookup", "Range Scans (e.g., Dates)", "Large Table Search", "Frequent Updates"],
        "Standard B-Tree": ["Perfect (O(log n))", "Good (Random I/O)", "Efficient", "No extra overhead"],
        "Clustered Index": ["Overkill", "Best (Sequential I/O)", "Best (Sequential I/O)", "High overhead (Rewrites table)"]
    }
    st.table(pd.DataFrame(cluster_logic))

    col_a, col_b = st.columns(2)
    with col_a:
        st.success("""
        **✅ When to use Clustered Index:**
        * On columns frequently used in `ORDER BY` or `WHERE x BETWEEN y`.
        * On static/historical tables (like `lap_times`) that don't change often.
        * On the most queried column (only ONE clustered index per table).
        """)
    with col_b:
        st.error("""
        **❌ When NOT to use:**
        * On tables with high `INSERT/UPDATE` volume (rewriting is slow).
        * On small tables where a full scan is fast enough.
        * If you can't afford downtime for the `CLUSTER` command lock.
        """)

    with st.expander("🔍 View Benchmarked SQL & Table Metadata"):
        st.markdown("**Benchmark Target:** `lap_times` table (approx. 600,000 rows)")
        st.code("SELECT * FROM lap_times WHERE driverid = 4;", language="sql")
        st.dataframe(df_lap, use_container_width=True)

except Exception as e:
    st.error(f"🚨 Section 2 Error: {e}")