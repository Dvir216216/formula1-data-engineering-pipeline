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

    # 2. Extract specific KPI values safely (Strict Filtering)
    baseline_df = df_mv[df_mv['scenario'].str.contains('Case 1', na=False, case=False)]
    mv_df = df_mv[df_mv['scenario'].str.contains('Case 5', na=False, case=False)]

    if baseline_df.empty or mv_df.empty:
        st.error("🚨 Data Contract Error: Could not find Case 1 or Case 5.")
        st.stop()

    baseline_time = baseline_df['execution_time_ms'].values[0]
    mv_time = mv_df['execution_time_ms'].values[0]

    # 3. Render Top Metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Baseline Execution Time", f"{baseline_time} ms")
    
    # Calculate performance improvement percentage
    improvement = round((baseline_time - mv_time) / baseline_time * 100, 2)
    col2.metric("Optimized Execution Time", f"{mv_time} ms", f"-{improvement}% Latency", delta_color="inverse")

    # 4. Render Dual-Axis Chart
    fig = go.Figure()
    
    # Bar for Execution Time (Left Y-Axis)
    fig.add_trace(go.Bar(
        x=df_mv['scenario'], 
        y=df_mv['execution_time_ms'], 
        name="Execution Time (ms)", 
        marker_color='#ef553b'
    ))
    
# Line chart for Query Cost (Right Y-Axis) - Floats over the bars
    fig.add_trace(go.Scatter(
        x=df_mv['scenario'], 
        y=df_mv['cost_estimate'], 
        name="Query Cost (I/O & CPU)", 
        mode='lines+markers',
        line=dict(color='#636efa', width=3),
        marker=dict(size=8),
        yaxis='y2'
    ))

    # Layout configuration for dual axes
    fig.update_layout(
        title="Raw SQL vs. Materialized View Performance",
        yaxis=dict(title="Execution Time (ms)", range=[0, 5]), # קיבוע הציר ל-5 מילישניות
        yaxis2=dict(title="Cost Estimate", overlaying='y', side='right', rangemode='tozero'), # יישור ציר ימין לאפס
        barmode='group',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    st.plotly_chart(fig, use_container_width=True)

    # --- Section 1: Transparency (SQL & Raw Data) ---
    with st.expander("🔍 View SQL Queries & Raw Benchmark Data"):
        st.markdown("**The Queries**")
        st.code("""-- Case 1: Real-Time Join (Baseline CPU Heavy)
    SELECT * FROM results res 
    JOIN races r ON res.raceid = r.raceid 
    JOIN drivers d ON res.driverid = d.driverid 
    JOIN constructors con ON res.constructorid = con.constructorid
    JOIN circuits c ON r.circuitid = c.circuitid
    WHERE d.driverid = 1;

    -- Case 5: Pre-computed Materialized View (Zero Join Overhead)
    SELECT * FROM mv_race_complete_details WHERE driverid = 1;""", language="sql")
        
        st.markdown("**Raw Benchmark Results**")
        st.dataframe(df_mv, use_container_width=True)
    
except FileNotFoundError:
    st.error("🚨 Error: The benchmark CSV file was not found. Please check the file path.")
except Exception as e:
    st.error(f"🚨 An error occurred while processing the data: {e}")


# --- Section 2: Clustered Indexing ---
st.divider()
st.header("2. Optimizing Disk I/O: Clustered Indexing")
st.markdown("Evaluating the impact of physical data arrangement on the disk. We measured a standard search query on the massive `lap_times` table.")

try:
    # 1. Load Data (Dynamic Path)
    idx_csv_path = os.path.join(BASE_DIR, 'data', 'benchmarks', 'benchmark_indexes.csv')
    df_idx = pd.read_csv(idx_csv_path)

    # Filter strictly for the Lap Times search to avoid mixing data
    df_lap = df_idx[df_idx['query_name'] == 'Lap Times Search']

    if df_lap.empty:
        st.error("🚨 Data Contract Error: Could not find 'Lap Times Search' queries in the CSV.")
        st.stop()

    # 2. Extract specific KPI values safely
    no_idx_time = df_lap.loc[df_lap['scan_type'].str.contains('No Index', na=False, case=False), 'execution_time_ms'].values[0]
    std_idx_time = df_lap.loc[df_lap['scan_type'].str.contains('Standard Index', na=False, case=False), 'execution_time_ms'].values[0]
    clustered_time = df_lap.loc[df_lap['scan_type'].str.contains('Clustered Index', na=False, case=False), 'execution_time_ms'].values[0]

    # 3. Render Top Metrics
    c1, c2, c3 = st.columns(3)
    c1.metric("1. Baseline (Seq Scan)", f"{no_idx_time} ms")
    
    imp_std = round((no_idx_time - std_idx_time) / no_idx_time * 100, 1)
    c2.metric("2. Standard B-Tree Index", f"{std_idx_time} ms", f"-{imp_std}% Latency", delta_color="inverse")
    
    imp_cluster = round((std_idx_time - clustered_time) / std_idx_time * 100, 1)
    c3.metric("3. Clustered Index", f"{clustered_time} ms", f"-{imp_cluster}% vs Standard", delta_color="inverse")

    # 4. Render Dual-Axis Chart
    fig2 = go.Figure()
    
    # Bar for Execution Time
    fig2.add_trace(go.Bar(
        x=df_lap['scan_type'], 
        y=df_lap['execution_time_ms'], 
        name="Execution Time (ms)", 
        marker_color='#ef553b'
    ))
    
    # Line for Query Cost (Floats above)
    fig2.add_trace(go.Scatter(
        x=df_lap['scan_type'], 
        y=df_lap['cost_estimate'], 
        name="Query Cost (Pages Read)", 
        mode='lines+markers',
        line=dict(color='#636efa', width=3),
        marker=dict(size=8),
        yaxis='y2'
    ))

    # Layout configuration
    fig2.update_layout(
        title="Disk I/O Optimization: Sequential vs. Random Reads",
        yaxis=dict(title="Execution Time (ms)", rangemode='tozero'),
        yaxis2=dict(title="Cost Estimate", overlaying='y', side='right', rangemode='tozero'),
        barmode='group',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    
    st.plotly_chart(fig2, use_container_width=True)

    # 5. The "Money Shot" Architectural Explanation
    st.info("""
    💡 **Architectural Insight:** Notice how the **Query Cost** stays identical between the Standard Index and the Clustered Index (4,858.96). 
    This occurs because PostgreSQL reads the exact same number of data pages in both scenarios. The 83% speed upgrade in the Clustered Index comes entirely from transforming **Random I/O** (jumping around the physical disk) into **Sequential I/O** (reading contiguous data blocks).
    """)

    # --- Section 2: Transparency (SQL & Raw Data) ---
    with st.expander("🔍 View SQL Queries & Raw Benchmark Data"):
        st.markdown("**The Query (Same query, different physical disk layout)**")
        st.code("""-- Finding all lap times for Driver 4
        SELECT * FROM lap_times WHERE driverid = 4;""", language="sql")
        st.markdown("**Raw Benchmark Results**")
        st.dataframe(df_lap, use_container_width=True)


except FileNotFoundError:
    st.error("🚨 Error: The benchmark_indexes.csv file was not found in data/benchmarks/.")
except Exception as e:
    st.error(f"🚨 An error occurred while processing the index data: {e}")