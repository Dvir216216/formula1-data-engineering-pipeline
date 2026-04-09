/* =============================================================================
QUERY: Average Lap Time per Track by Active Constructors
=============================================================================
Purpose: 
- Identifies currently active F1 teams to filter out obsolete/renamed teams.
- Calculates the average fastest lap time for each team on each track.
- Focuses on the Hybrid Era (2014+) for relevant performance comparison.
*/

WITH active_teams AS (
    -- Step 1: Identify teams that competed in the most recent season available in the dataset
    -- This ensures we only analyze teams relevant to the current grid.
    SELECT DISTINCT constructorid
    FROM v_race_complete_details
    WHERE year = (SELECT MAX(year) FROM v_race_complete_details)
),

team_stats AS (
    -- Step 2: Aggregation of lap times per circuit and constructor
    SELECT 
        v.circuit_name,
        v.constructor_name,
        -- Format the average time interval into a readable string (MM:SS.MS)
        TO_CHAR(AVG(CAST('00:' || v.fastestlaptime AS INTERVAL)), 'MI:SS.MS') AS avg_lap_time,
        -- Count valid lap times to measure data reliability (Sample Size)
        COUNT(v.fastestlaptime) AS sample_size
    FROM 
        v_race_complete_details v
    WHERE 
        v.year >= 2014 -- Filter: Hybrid Era only
        AND v.fastestlaptime IS NOT NULL -- Safety: Exclude rows with missing timing data
        AND v.constructorid IN (SELECT constructorid FROM active_teams) -- Filter: Keep only active teams
    GROUP BY 
        v.circuit_name, 
        v.constructor_name
)

-- Step 3: Final Output selection
SELECT * FROM team_stats
ORDER BY 
    circuit_name ASC,      -- Organize results by track context
    avg_lap_time ASC;      -- Rank teams from fastest to slowest