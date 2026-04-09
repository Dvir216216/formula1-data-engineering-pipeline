-- ==========================================================
-- STEP 2: Baseline Measurement (The "Before" State)
-- We run heavy queries on the raw table to see how slow it is.
-- ==========================================================

-- 1. Run a search on a non-indexed column (DriverID 4)
-- This forces PostgreSQL to scan all 600,000 rows (Seq Scan).
SELECT measure_query(
    'SELECT * FROM lap_times WHERE driverid = 4', 
    'Baseline: Filter DriverID (No Index)', 
    FALSE
);

-- 2. View the logs to see the slow time
SELECT * FROM benchmark_logs ORDER BY log_id DESC LIMIT 1;