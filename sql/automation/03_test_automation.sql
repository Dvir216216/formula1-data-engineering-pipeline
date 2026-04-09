-- ==============================================================================
-- Automation: Verification Test
-- Purpose: Prove that inserting data into 'results' automatically updates the View.
-- ==============================================================================

-- 1. Check current count in the Materialized View (Before)
SELECT COUNT(*) AS count_before FROM mv_race_complete_details;

-- 2. Insert a DUMMY record into the raw 'results' table
-- We use a fake raceId (0) and driverId (1) just for testing.
INSERT INTO results (resultid, raceid, driverid, constructorid, number, grid, position, points, laps, statusid)
VALUES (999999, 18, 1, 1, 44, 1, 1, 25, 58, 1);

-- 3. Check count again (After)
-- If the Trigger works, this count should be +1 immediately.
SELECT COUNT(*) AS count_after FROM mv_race_complete_details;

-- 4. Cleanup (Delete the dummy record)
-- The trigger will fire again here and update the view back to original state.
DELETE FROM results WHERE resultid = 999999;