/*
=============================================================================
PROJECT: Formula 1 Data Analysis
FILE: 00_init_database_schema.sql
AUTHOR: [Your Name]
DESCRIPTION: 
    This script initializes the PostgreSQL database schema for the F1 project.
    It performs a clean reset (DROPS existing tables) and recreates them
    with the correct data types and relationships.
    
    USAGE: Run this script once to set up the structure before importing CSV data.
=============================================================================
*/

-- ==========================================
-- 1. CLEANUP SECTION
-- ==========================================
-- We use CASCADE to remove dependent tables automatically. 
-- This ensures a fresh start every time this script is run.

DROP TABLE IF EXISTS lap_times CASCADE;
DROP TABLE IF EXISTS qualifying CASCADE;
DROP TABLE IF EXISTS pit_stops CASCADE;
DROP TABLE IF EXISTS sprint_results CASCADE;
DROP TABLE IF EXISTS results CASCADE;
DROP TABLE IF EXISTS driver_standings CASCADE;
DROP TABLE IF EXISTS constructor_standings CASCADE;
DROP TABLE IF EXISTS constructor_results CASCADE;
DROP TABLE IF EXISTS races CASCADE;
DROP TABLE IF EXISTS drivers CASCADE;
DROP TABLE IF EXISTS constructors CASCADE;
DROP TABLE IF EXISTS status CASCADE;
DROP TABLE IF EXISTS seasons CASCADE;
DROP TABLE IF EXISTS circuits CASCADE;



-- ==========================================
-- 2. MASTER TABLES CREATION (Parent Tables)
-- ==========================================

-- Circuits: Lookup table for race tracks
CREATE TABLE circuits (
    circuitId INT PRIMARY KEY,
    circuitRef VARCHAR(255),
    name VARCHAR(255),
    location VARCHAR(255),
    country VARCHAR(255),
    lat NUMERIC,
    lng NUMERIC,
    alt INT,
    url VARCHAR(255)
);

-- Seasons: Lookup table for championship years
CREATE TABLE seasons (
    year INT PRIMARY KEY,
    url VARCHAR(255)
);

-- Status: Lookup table for race result status (Finished, Collision, etc.)
CREATE TABLE status (
    statusId INT PRIMARY KEY,
    status VARCHAR(255)
);

-- Constructors: The F1 teams
CREATE TABLE constructors (
    constructorId INT PRIMARY KEY,
    constructorRef VARCHAR(255),
    name VARCHAR(255),
    nationality VARCHAR(255),
    url VARCHAR(255)
);

-- Drivers: The athletes
CREATE TABLE drivers (
    driverId INT PRIMARY KEY,
    driverRef VARCHAR(255),
    number INT, -- Driver's permanent number
    code VARCHAR(10),
    forename VARCHAR(255),
    surname VARCHAR(255),
    dob DATE,
    nationality VARCHAR(255),
    url VARCHAR(255)
);


-- ==========================================
-- 3. CORE OPERATIONAL TABLES
-- ==========================================

-- Races: Connects a specific year and circuit
CREATE TABLE races (
    raceId INT PRIMARY KEY,
    year INT REFERENCES seasons(year),
    round INT,
    circuitId INT REFERENCES circuits(circuitId),
    name VARCHAR(255),
    date DATE,
    time TIME, -- Can be NULL for older races
    url VARCHAR(255),
    fp1_date DATE,
    fp1_time TIME,
    fp2_date DATE,
    fp2_time TIME,
    fp3_date DATE,
    fp3_time TIME,
    quali_date DATE,
    quali_time TIME,
    sprint_date DATE,
    sprint_time TIME
);


-- ==========================================
-- 4. PERFORMANCE & RESULTS TABLES (Child Tables)
-- ==========================================

CREATE TABLE constructor_results (
    constructorResultsId INT PRIMARY KEY,
    raceId INT REFERENCES races(raceId),
    constructorId INT REFERENCES constructors(constructorId),
    points NUMERIC, -- Using NUMERIC to handle half-points history
    status VARCHAR(255) -- Usually null in raw data, can be ignored or mapped
);

CREATE TABLE constructor_standings (
    constructorStandingsId INT PRIMARY KEY,
    raceId INT REFERENCES races(raceId),
    constructorId INT REFERENCES constructors(constructorId),
    points NUMERIC,
    position INT,
    positionText VARCHAR(50), -- VARCHAR because position can be 'DQ' or 'E'
    wins INT
);

CREATE TABLE driver_standings (
    driverStandingsId INT PRIMARY KEY,
    raceId INT REFERENCES races(raceId),
    driverId INT REFERENCES drivers(driverId),
    points NUMERIC,
    position INT,
    positionText VARCHAR(50),
    wins INT
);

CREATE TABLE results (
    resultId INT PRIMARY KEY,
    raceId INT REFERENCES races(raceId),
    driverId INT REFERENCES drivers(driverId),
    constructorId INT REFERENCES constructors(constructorId),
    number INT,
    grid INT, -- Starting position
    position INT, -- Finishing position (Official)
    positionText VARCHAR(50), -- Stores 'R' for retired, 'D' for disqualified
    positionOrder INT, -- Useful for sorting
    points NUMERIC,
    laps INT,
    time VARCHAR(255), -- VARCHAR: Time format varies wildly (+1 Lap, 1:20.000, etc.)
    milliseconds INT,
    fastestLap INT,
    rank INT,
    fastestLapTime VARCHAR(255), -- VARCHAR: Dirty data often contains '\N' or NULLs
    fastestLapSpeed VARCHAR(255), -- VARCHAR: Needs casting to NUMERIC for analysis
    statusId INT REFERENCES status(statusId)
);

CREATE TABLE sprint_results (
    resultId INT PRIMARY KEY,
    raceId INT REFERENCES races(raceId),
    driverId INT REFERENCES drivers(driverId),
    constructorId INT REFERENCES constructors(constructorId),
    number INT,
    grid INT,
    position INT,
    positionText VARCHAR(50),
    positionOrder INT,
    points NUMERIC,
    laps INT,
    time VARCHAR(255),
    milliseconds INT,
    fastestLap INT,
    fastestLapTime VARCHAR(255),
    statusId INT REFERENCES status(statusId)
);

CREATE TABLE pit_stops (
    raceId INT REFERENCES races(raceId),
    driverId INT REFERENCES drivers(driverId),
    stop INT,
    lap INT,
    time TIME,
    duration VARCHAR(50), -- VARCHAR: Sometimes includes text or errors
    milliseconds INT,
    PRIMARY KEY (raceId, driverId, stop) -- Composite Primary Key
);

CREATE TABLE qualifying (
    qualifyId INT PRIMARY KEY,
    raceId INT REFERENCES races(raceId),
    driverId INT REFERENCES drivers(driverId),
    constructorId INT REFERENCES constructors(constructorId),
    number INT,
    position INT,
    q1 VARCHAR(50), -- Text to handle empty strings or non-time formats
    q2 VARCHAR(50),
    q3 VARCHAR(50)
);

CREATE TABLE lap_times (
    raceId INT REFERENCES races(raceId),
    driverId INT REFERENCES drivers(driverId),
    lap INT,
    position INT,
    time VARCHAR(50), -- Lap time textual representation
    milliseconds INT, -- The absolute truth for calculations
    PRIMARY KEY (raceId, driverId, lap) -- Composite Primary Key
);

