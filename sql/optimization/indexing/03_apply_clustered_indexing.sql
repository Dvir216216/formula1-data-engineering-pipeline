-- ==============================================================================
-- Optimization Step 3: Apply Indexing Strategy
-- Purpose: Create the index and physically reorder the table (CLUSTER) for speed.
-- ==============================================================================

-- 1. Idempotency: Remove existing index if it exists to allow re-running.
DROP INDEX IF EXISTS idx_lap_times_driverid;

-- 2. Create the B-Tree Index
-- This creates a logical map pointing to rows by driverId.
CREATE INDEX idx_lap_times_driverid 
ON lap_times(driverid);

-- 3. Perform Clustering (The "Secret Sauce")
-- This command physically re-writes the table to disk, ordering rows by driverId.
-- Result: The engine reads fewer disk pages because all data for Driver X is adjacent.
CLUSTER lap_times USING idx_lap_times_driverid;

-- 4. Update Statistics
-- Ensures the Query Planner knows about the new data distribution immediately.
ANALYZE lap_times;