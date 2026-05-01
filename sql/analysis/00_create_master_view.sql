/* =============================================================================
* File Name: 00_create_master_view.sql
* Purpose: Creates a master view joining the core tables to serve as the Single Source of Truth for downstream analytics.
* Dependencies: races, circuits, results, drivers, status, constructors
* Key Logic / Transformations: Joins 6 core tables, cleanses data by standardizing Kaggle '\N' strings to native SQL NULLs.
* Author: Dvir
* ============================================================================= */

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

    -- Constructor Info
    con.constructorid,
    con.name AS constructor_name,
    con.nationality AS constructor_nationality,
    
    -- Results & Status
    res.resultid,
    res.grid,          
    res.positionorder, 
    res.points,
    res.laps,
    -- Data Cleansing: Standardizing Kaggle '\N' to actual NULLs
    NULLIF(res.fastestlaptime, '\N') AS fastestlaptime,
    NULLIF(res.fastestlapspeed, '\N') AS fastestlapspeed,
    res.statusid,
    s.status AS status_text 

FROM races r
JOIN circuits c ON r.circuitid = c.circuitid
JOIN results res ON r.raceid = res.raceid
JOIN drivers d ON res.driverid = d.driverid
JOIN status s ON res.statusid = s.statusid
JOIN constructors con ON res.constructorid = con.constructorid;