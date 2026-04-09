-- ==============================================================================
-- Automation: Database Trigger
-- Purpose: The 'Listener' that fires the refresh function automatically.
-- ==============================================================================

-- 1. Clean up old trigger if exists
DROP TRIGGER IF EXISTS trg_results_update ON results;

-- 2. Create the Trigger
-- Fires ONLY ONCE per insert batch (Statement Level), not per row.
CREATE TRIGGER trg_results_update
AFTER INSERT OR UPDATE OR DELETE ON results
FOR EACH STATEMENT
EXECUTE FUNCTION refresh_f1_dashboard();