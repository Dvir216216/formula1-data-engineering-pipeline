# 🚀 Materialized Views & Pre-computation Strategy

This module tackles the performance bottleneck of **Complex JOINs**.
While Indexing solves search problems, it does not solve computational complexity. [cite_start]Here, we demonstrate how **Materialized Views** reduce execution time by **94%**[cite: 61].

## 🧪 The Challenge: The "Join Overhead"
Querying race results requires joining 5 tables (`Results` ↔ `Races` ↔ `Drivers` ↔ `Constructors` ↔ `Circuits`).
[cite_start]Standard indexes failed to improve performance because the database engine still had to "stitch" these tables together for every single query [cite: 80-81].

## 📊 Benchmark Results
*Data extracted from `benchmark_results.csv`*

| Scenario | Strategy | Execution Time | Cost Estimate | Insight |
| :--- | :--- | :--- | :--- | :--- |
| **Case 1** | Raw SQL (Baseline) | **2.78 ms** | 738.95 | High CPU load due to real-time joins. |
| **Case 2** | Standard View | **2.69 ms** | 743.12 | "Syntactic Sugar" - no performance gain. |
| **Case 5** | **Materialized View + Index** | **0.16 ms** | **8.32** | **94% Faster. Instant retrieval.** |

## 🛠️ Implementation
* **`01_create_materialized_view.sql`**: Creates a physical snapshot of the joined data (`mv_race_complete_details`) and indexes it.
* **`02_run_comparative_benchmark.sql`**: Executes the comparative analysis using the measurement tool.

## 💡 Key Takeaway
[cite_start]Use Materialized Views for **read-heavy** workloads where complex aggregations or joins are required, and slight data staleness (e.g., "Data as of last night") is acceptable [cite: 96-99].