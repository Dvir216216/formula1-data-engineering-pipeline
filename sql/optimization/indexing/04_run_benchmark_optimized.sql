-- ==============================================================================
-- Optimization Step 4: Verify Performance Gains
-- Purpose: Re-run the exact same queries to measure the speedup after Indexing.
-- ==============================================================================

-- 1. Test Case A: Simple Filtering (Re-Test)
-- Now, the engine should use the 'idx_lap_times_driverid' index.
-- Expected Result: Execution time drops from ~40ms to ~3ms (92% improvement).
SELECT measure_query(
    'SELECT * FROM lap_times WHERE driverid = 4', 
    'Optimized: Filter by DriverID (Clustered Index)', 
    TRUE
);

-- 2. Test Case B: Aggregation (Re-Test)
-- Even for aggregations, the clustered index reduces I/O.
SELECT measure_query(
    'SELECT raceid, AVG(milliseconds) FROM lap_times GROUP BY raceid', 
    'Optimized: Group By RaceID (Index Scan)', 
    TRUE
);

-- 3. FINAL REPORT: Compare Before vs. After
-- This query shows the "Money Shot" - the difference in milliseconds.
SELECT 
    scenario_name, 
    execution_time_ms, 
    cost_estimate,
    notes 
FROM benchmark_logs 
ORDER BY log_id DESC 
LIMIT 4;