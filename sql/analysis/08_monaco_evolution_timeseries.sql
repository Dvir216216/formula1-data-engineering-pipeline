/* ====================================================
QUERY: Monaco Circuit Evolution (Time Series Analysis)
=======================================================
Purpose:
- Analyzes the progression of lap times over the last two decades.
- Compares the absolute best lap (Peak Performance) vs. the field average
  to understand the impact of car regulations and technology on speed.

Key Filters:
- Circuit: 'Circuit de Monaco' (Chosen for its historical layout consistency).
- Data Range: 2004 onwards (Reliable digital timing era).
*/

WITH yearly_stats AS (
    -- Step 1: Calculate raw stats per year (The code we fixed)
    SELECT 
        v.year,
        MIN(CAST(v.fastestlaptime AS INTERVAL)) AS best_race_lap,
        AVG(CAST(v.fastestlaptime AS INTERVAL)) AS avg_lap_time
    FROM 
        v_race_complete_details v
    WHERE 
        v.circuit_name = 'Circuit de Monaco'
        AND v.fastestlaptime IS NOT NULL
        AND v.year >= 2004
    GROUP BY 
        v.year
)

-- Step 2: Calculate the difference from the previous year
SELECT 
    year,
    best_race_lap,
    best_race_lap - LAG(best_race_lap) OVER (ORDER BY y.year) AS best_lap_diff,
    avg_lap_time,
    avg_lap_time - LAG(avg_lap_time) OVER (ORDER BY y.year) AS avg_lap_diff
FROM 
    yearly_stats y
ORDER BY 
    y.year;
