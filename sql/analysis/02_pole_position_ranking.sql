-- Top 10 leaders in pole position on every circuit -- 

WITH PolePositionData AS (
	SELECT 
		c.circuitref, 
		d.driverref, 
		COUNT(*) as pole_1_count,
		DENSE_RANK() OVER (PARTITION BY c.circuitref ORDER BY COUNT(*) DESC) as rank_in_circuit
	FROM circuits c
	JOIN races ra ON c.circuitid = ra.circuitid
	JOIN results re ON ra.raceid = re.raceid
	JOIN drivers d ON d.driverid = re.driverid
	WHERE re.grid = 1
	GROUP BY c.circuitref, d.driverref
)
SELECT 
    circuitref,
    driverref,
    pole_1_count,
    rank_in_circuit
FROM PolePositionData
WHERE rank_in_circuit <= 3 AND pole_1_count >= 2;