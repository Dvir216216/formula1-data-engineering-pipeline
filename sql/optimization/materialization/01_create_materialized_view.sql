-- ==============================================================================
-- Optimization Strategy: Materialized View (Pre-computation)
-- Problem: Heavy JOINs across 5 tables (Results, Races, Drivers, etc.) refer to[cite: 60].
-- Solution: Pre-calculate the join and store it physically using a Materialized View.
-- ==============================================================================

-- 1. Cleanup: Remove existing views to ensure idempotency
DROP MATERIALIZED VIEW IF EXISTS mv_race_complete_details CASCADE;
DROP VIEW IF EXISTS v_race_complete_details CASCADE;

-- 2. Create the Materialized View (The "Physical Snapshot")
-- This query executes ONCE at creation time, not at runtime [cite: 86-88].
CREATE MATERIALIZED VIEW mv_race_complete_details AS
SELECT 
    r.raceid,
    r.year,
    r.name AS race_name,
    c.name AS circuit_name,
    d.driverid,
    d.forename || ' ' || d.surname AS driver_name,
    res.positionorder,
    res.points,
    cons.name AS constructor_name
FROM results res
JOIN races r ON res.raceid = r.raceid
JOIN drivers d ON res.driverid = d.driverid
JOIN constructors cons ON res.constructorid = cons.constructorid
JOIN circuits c ON r.circuitid = c.circuitid;

-- 3. The "Holy Grail": Indexing the Materialized View
-- Unlike a standard view, we can place an index directly on the result[cite: 89].
CREATE INDEX idx_mv_race_details_driver 
ON mv_race_complete_details(driverid);

-- 4. Gather Statistics
ANALYZE mv_race_complete_details;