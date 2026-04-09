/* =============================================================================
VIEW SETUP: v_race_complete_details
=============================================================================
Purpose: 
- Creates a master view joining the core 4 tables + status table.
- This view will serve as the "Single Source of Truth" for future queries.
- It handles the complex joins once, so we don't have to repeat them.
*/

CREATE OR REPLACE VIEW v_race_complete_details AS
SELECT 
    -- Race & Circuit Info
    r.raceid,
    r.year,
    r.date AS race_date,
    c.circuitid,
    c.name AS circuit_name,
    c.location,
    c.country,
    
    -- Driver Info
    d.driverid,
    d.driverref,
    d.code AS driver_code,
    d.dob AS driver_dob,
    d.nationality AS driver_nationality,
    
    -- Results & Status
    res.resultid,
    res.grid,          -- Starting position
    res.positionorder, -- Finishing position (Official)
    res.points,
    res.laps,
    res.fastestlaptime,
    res.fastestlapspeed,
    res.statusid,
    s.status AS status_text -- 'Finished', 'Collision', '+1 Lap', etc.

FROM races r
JOIN circuits c ON r.circuitid = c.circuitid
JOIN results res ON r.raceid = res.raceid
JOIN drivers d ON res.driverid = d.driverid
JOIN status s ON res.statusid = s.statusid;