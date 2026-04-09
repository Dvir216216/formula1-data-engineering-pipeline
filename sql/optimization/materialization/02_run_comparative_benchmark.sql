-- ==============================================================================
-- Benchmark: Comparing Optimization Strategies for Complex JOINs
-- We verify that standard indexing fails on heavy joins, while Materialization succeeds.
-- ==============================================================================

-- Case 1: Raw SQL (Baseline) - The engine must join 5 tables in real-time.
SELECT measure_query(
    'SELECT * FROM results res 
     JOIN races r ON res.raceid = r.raceid 
     JOIN drivers d ON res.driverid = d.driverid 
     WHERE d.driverid = 1', 
    'Case 1: Raw SQL Join (Baseline)', 
    FALSE
);

-- Case 2: Standard View (Virtualization) - "Syntactic Sugar", same performance overhead[cite: 68].
SELECT measure_query(
    'SELECT * FROM v_race_complete_details WHERE driverid = 1', 
    'Case 2: Standard View (Virtual)', 
    FALSE
);

-- Case 5: Materialized View + Index (The Solution) - Zero Joins, Instant Lookup [cite: 90-91].
SELECT measure_query(
    'SELECT * FROM mv_race_complete_details WHERE driverid = 1', 
    'Case 5: Materialized View + Index', 
    TRUE
);

-- Show the final scoreboard
SELECT scenario_name, execution_time_ms, cost_estimate 
FROM benchmark_logs 
ORDER BY log_id DESC LIMIT 3;