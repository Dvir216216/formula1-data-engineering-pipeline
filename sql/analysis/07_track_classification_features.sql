/* 
QUERY: Circuit Classification (Feature Engineering)

Purpose: 
- Calculates average speed per track (based on fastest laps).
- Classifies tracks into 3 categories: High Speed, Balanced, Technical.
*/

WITH track_stats AS (
	SELECT
		v.circuit_name,
		AVG(CAST(v.fastestlapspeed AS NUMERIC)) AS avg_speed_kph
	FROM 
		v_race_complete_details as v
	WHERE
		v.year >= 2014
		AND v.fastestlapspeed IS NOT NULL
	GROUP BY 
		v.circuit_name 
),

track_types AS (
SELECT 
	t.circuit_name,
	ROUND(t.avg_speed_kph , 2) AS avg_speed,
	CASE
		WHEN t.avg_speed_kph > 210 THEN 'High_Speed'
		WHEN t.avg_speed_kph < 180 THEN 'Technical'
		ELSE 'Balanced'
	END AS circuit_type
FROM 
	track_stats t
ORDER BY
	t.avg_speed_kph DESC
)

SELECT 
	t.circuit_type,
	v.driverref,
	COUNT(*) AS wins
FROM 
	track_types t JOIN v_race_complete_details v ON t.circuit_name = v.circuit_name
WHERE 
	positionorder = 1
GROUP BY
	t.circuit_type, 
	v.driverref
ORDER BY 
    wins DESC


