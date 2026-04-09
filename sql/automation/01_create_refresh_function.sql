-- ==============================================================================
-- Automation: Refresh Materialized View Logic
-- Purpose: Defines 'What to do' when data changes.
-- ==============================================================================

CREATE OR REPLACE FUNCTION refresh_f1_dashboard()
RETURNS TRIGGER AS $$
BEGIN
    -- Refresh the materialized view to show the latest data.
    -- We use 'CONCURRENTLY' (optional) if we have a unique index, 
    -- allowing users to read the view while it updates.
    REFRESH MATERIALIZED VIEW mv_race_complete_details;
    
    RETURN NULL; -- Result is ignored for statement-level triggers
END;
$$ LANGUAGE plpgsql;