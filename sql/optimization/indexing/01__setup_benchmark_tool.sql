-- ==============================================================================
-- Optimization Module: Benchmark Logging
-- Purpose: Creates a table to store performance metrics (Time/Cost) for A/B testing.
-- ==============================================================================

-- 1. Safe Initialization: Drop the table if it already exists to start fresh.
DROP TABLE IF EXISTS benchmark_logs CASCADE;

-- 2. Create the Benchmark Table
CREATE TABLE benchmark_logs (
    log_id            SERIAL PRIMARY KEY,
    test_name         VARCHAR(100) NOT NULL, 
    has_index         BOOLEAN,               
    execution_time_ms NUMERIC(10, 3),
    cost_estimate     NUMERIC(10, 2),
    log_time          TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


/*
 * FUNCTION: measure_query
 * -----------------------
 * Description: Executes a dynamic SQL query using EXPLAIN ANALYZE, 
 * extracts performance metrics (Time & Cost), and logs them into a table.
 * * Parameters:
 * - p_query_sql (TEXT): The SQL query string to be executed and measured.
 * - p_test_name (TEXT): A descriptive name for the test case (e.g., 'Driver Search').
 * - p_has_index (BOOL): Flag indicating if an index exists for this test context.
 * * Returns: VOID
 */

CREATE OR REPLACE FUNCTION measure_query(p_query_sql TEXT, p_test_name TEXT, p_has_index BOOLEAN)
RETURNS VOID 
AS $$
DECLARE
    v_explain_json JSONB;
    v_exec_time NUMERIC;
    v_cost NUMERIC;
BEGIN
	-- Execute dynamic query and capture JSON	EXECUTE
		'EXPLAIN (ANALYZE, FORMAT JSON) ' || p_query_sql
	INTO v_explain_json;
	
	-- Extract specific metrics
    v_exec_time := (v_explain_json->0->>'Execution Time')::NUMERIC;
    v_cost := (v_explain_json->0->'Plan'->>'Total Cost')::NUMERIC;

    -- Log results into the benchmark table (Columns match exactly now)
    INSERT INTO benchmark_logs (test_name, has_index, execution_time_ms, cost_estimate)
    VALUES (p_test_name, p_has_index, v_exec_time, v_cost);

    RAISE NOTICE 'Test "%" logged.', p_test_name;
END;
$$ LANGUAGE plpgsql;