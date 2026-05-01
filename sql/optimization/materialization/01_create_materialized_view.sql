-- ==============================================================================
-- Optimization Strategy: Materialized View & Indexing
-- ==============================================================================

-- 1. Cleanup
DROP MATERIALIZED VIEW IF EXISTS mv_race_complete_details CASCADE;

-- 2. Create the Materialized View (The "Physical Snapshot")
-- Pulling directly from our highly optimized Master View to prevent code duplication
CREATE MATERIALIZED VIEW mv_race_complete_details AS
SELECT * FROM v_race_complete_details;

-- 3. Required Index for Automation (Concurrent Refresh)
-- This ensures we can update the data in the background without locking the Streamlit app
CREATE UNIQUE INDEX idx_mv_resultid ON mv_race_complete_details (resultid);

-- 4. Analytical Index (The one you originally created)
-- Speeds up queries that filter or group by driver
CREATE INDEX idx_mv_race_details_driver ON mv_race_complete_details(driverid);

-- 5. Gather Statistics
ANALYZE mv_race_complete_details;