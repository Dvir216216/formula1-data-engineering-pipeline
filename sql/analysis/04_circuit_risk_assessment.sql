/*
Query 4 (Refactored using VIEW): Most dangerous tracks
Using the 'v_race_complete_details' view created in setup.
*/

SELECT 
    circuit_name,
    COUNT(*) AS dnf_count
FROM v_race_complete_details 
WHERE 
    status_text <> 'Finished' 
    AND status_text NOT LIKE '+%'
GROUP BY circuit_name
ORDER BY dnf_count DESC
LIMIT 5;