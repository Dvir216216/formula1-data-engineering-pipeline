SELECT 
    v.circuit_name,
    -- Formatted average lap time
    TO_CHAR(AVG(CAST('00:' || v.fastestlaptime AS INTERVAL)), 'MI:SS.MS') AS avg_lap_time,
    -- Count how many valid lap times were used for this calculation
    COUNT(v.fastestlaptime) AS sample_size
FROM 
    v_race_complete_details AS v
WHERE 
    v.year >= 2014 -- Hybrid Era
    AND v.fastestlaptime IS NOT NULL
GROUP BY 
    v.circuit_name
ORDER BY 
    -- Sort by reliability (sample size) to see the most established tracks first
    sample_size DESC;

