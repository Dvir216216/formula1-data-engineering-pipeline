import streamlit as st
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
    # 1. Load Data (עדכן את הנתיב במידת הצורך)
    df_mv = pd.read_csv("data/benchmark_results_2.csv")
    
    # 2. Extract specific KPI values safely
    baseline_time = df_mv.loc[df_mv['scenario_name'].str.contains('Baseline', na=False, case=False), 'execution_time_ms'].values[0]
    mv_time = df_mv.loc[df_mv['scenario_name'].str.contains('Materialized', na=False, case=False), 'execution_time_ms'].values[0]

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
        x=df_mv['scenario_name'], 
        y=df_mv['execution_time_ms'], 
        name="Execution Time (ms)", 
        marker_color='#ef553b'
    ))
    
    # Line/Bar for Query Cost (Right Y-Axis)
    fig.add_trace(go.Bar(
        x=df_mv['scenario_name'], 
        y=df_mv['cost_estimate'], 
        name="Query Cost (I/O & CPU)", 
        marker_color='#636efa', 
        yaxis='y2'
    ))

    # Layout configuration for dual axes
    fig.update_layout(
        title="Raw SQL vs. Materialized View Performance",
        yaxis=dict(title="Execution Time (ms)"),
        yaxis2=dict(title="Cost Estimate", overlaying='y', side='right'),
        barmode='group',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
except FileNotFoundError:
    st.error("🚨 Error: The benchmark CSV file was not found. Please check the file path.")
except Exception as e:
    st.error(f"🚨 An error occurred while processing the data: {e}")