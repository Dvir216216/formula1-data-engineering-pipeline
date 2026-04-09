# Advanced SQL Analytics & Insights

This directory demonstrates the transition from raw data to business intelligence.
[cite_start]Using the `v_race_complete_details` master view[cite: 16], we answer complex questions about Formula 1 history using advanced SQL techniques.

## Techniques Demonstrated

| Script | Business Question | Key SQL Concepts |
| :--- | :--- | :--- |
| **01 Popularity** | Which circuits are historical staples? | `GROUP BY`, `ORDER BY DESC` |
| **02 Ranking** | Who is the "King of Pole" at each track? | **Window Functions**: `DENSE_RANK() OVER (PARTITION BY)` |
| **03 Gap Analysis** | How large is the gap between the fastest lap and the runner-up? | **Time Series**: `LAG()`, `CAST(... AS INTERVAL)` |
| **04 Risk** | Which tracks have the highest accident rates? | **Logic**: `CASE WHEN`, Ratio Calculation |
| **06 Dominance** | Which constructors define the modern era? | **CTEs** (Common Table Expressions) |
| **08 Evolution** | How have lap times improved over 70 years? | **Trend Analysis**: Delta calculation |

##  How to Run

Since these queries are read-only analytics, you can run them in any order against the database.
Ensure you have run `00_create_master_view.sql` first, as most queries depend on it.