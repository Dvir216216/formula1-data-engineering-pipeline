
-- Top 10 circuits which had the most reces --
SELECT c.circuitid, c.name, COUNT (*)
FROM circuits c JOIN races r
ON c.circuitid = r.circuitid
GROUP BY c.circuitid, c.name
ORDER BY COUNT (*) DESC
LIMIT 10;