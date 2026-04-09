# ⚡ Database Indexing & Physical Storage Optimization

This module demonstrates the performance impact of different indexing strategies on large datasets (~600k rows).
We focus on the transition from **Sequential Scans** to **Clustered Index Scans**.

## 🧪 The Experiment
We tested query performance on the `lap_times` table using three storage configurations:
1.  **Heap Only**: No indexes (Baseline).
2.  **Standard Index**: Traditional B-Tree Index.
3.  **Clustered Index**: Physically reordering the table to match the index.

## 📊 Benchmark Results (Evidence)
*Data extracted from `benchmark_results.csv`*

| Strategy | Scan Type | Execution Time | Cost Estimate | Improvement |
| :--- | :--- | :--- | :--- | :--- |
| **Baseline** | Seq Scan | **39.46 ms** | 10,605 | - |
| **Optimization 1** | Standard Index | **18.81 ms** | 4,858 | 52% |
| **Optimization 2** | **Clustered Index** | **3.09 ms** | 4,858 | **92% (13x Faster)** |

> **Insight:** While the standard index reduced CPU time, the **Clustered Index** minimized I/O by ensuring that all laps for a specific driver are stored on adjacent disk pages.

## 📂 File Structure
* `01_setup_benchmark_tool.sql`: Creates the logging table and measurement function.
* `02_run_benchmark_baseline.sql`: Measures performance *before* optimization.
* `03_apply_clustered_indexing.sql`: Creates the index and runs the `CLUSTER` command.
* `04_run_benchmark_optimized.sql`: Measures performance *after* optimization.
* `benchmark_results.csv`: Raw log data from the experiment.