-- Top 10 circuits which had the most races --
SELECT 
    c.circuitid, 
    c.name, 
    COUNT(*) AS race_count 
FROM circuits c 
JOIN races r ON c.circuitid = r.circuitid
GROUP BY 
    c.circuitid, 
    c.name
ORDER BY 
    race_count DESC 
LIMIT 10;