/* Query: Top 3 Fastest Laps per Circuit (Refactored using VIEW)
Source: v_race_complete_details
Logic: 
- Casting text time to INTERVAL for gap analysis.
- Using Window Functions for ranking and gap calculation.
*/

WITH RawData AS (
    SELECT 
        -- Simply selecting columns from the View
        circuit_name,
        driverref,
        year AS record_year,
        fastestlaptime AS time_text,
        
        -- 1. Complex Logic: Convert text to INTERVAL
        CAST('00:' || fastestlaptime AS INTERVAL) AS lap_interval,
        
        -- 2. Window Function: Check track activity
        -- Note: We can partition by circuit_name directly from the view
        MAX(year) OVER (PARTITION BY circuit_name) AS last_race_year_at_circuit
        
    FROM v_race_complete_details  -- <--- HERE IS THE MAGIC! No Joins!
    
    WHERE fastestlaptime IS NOT NULL 
      AND fastestlaptime != '\N'
),

RankedData AS (
    SELECT 
        *,
        -- Rank drivers by fastest time (ASC)
        ROW_NUMBER() OVER (PARTITION BY circuit_name ORDER BY lap_interval ASC) as time_rank
    FROM RawData
)

SELECT 
    circuit_name,
    driverref,
    record_year,
    time_text,
    
    -- 3. Gap Analysis
    lap_interval - LAG(lap_interval) OVER (PARTITION BY circuit_name ORDER BY time_rank) AS gap_to_prev,
    
    last_race_year_at_circuit,
    
    -- Status Logic
    CASE 
        WHEN last_race_year_at_circuit >= 2023 THEN 'Active Track'
        WHEN record_year = last_race_year_at_circuit THEN 'Track Retired'
        ELSE 'Historical Record' 
    END AS track_status

FROM RankedData
WHERE time_rank <= 3
ORDER BY circuit_name, time_rank;