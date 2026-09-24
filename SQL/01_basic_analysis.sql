-- ============================================================
-- Industrial Compressor Energy Analytics
-- SQL Analysis - Basic Filtering & Sorting
-- ============================================================

-- 1. View sample records
SELECT * FROM compressor_data LIMIT 10;


-- 2. Find high-power compressor readings
SELECT * FROM compressor_data WHERE Power_kW > 30 ORDER BY Power_kW DESC LIMIT 10;


-- 3. Find highest-power readings for CP-05
SELECT * FROM compressor_data WHERE Compressor_ID = 'CP-05' ORDER BY Power_kW DESC LIMIT 10;


-- 4. Find readings with both high load and high power
SELECT * FROM compressor_data WHERE Load_Percent > 80 AND Power_kW > 30 ORDER BY Power_kW DESC;


-- 5. Find records containing missing sensor values
SELECT * FROM compressor_data WHERE Flow_m3h IS NULL OR Pressure_bar IS NULL OR Temperature_C IS NULL;


-- 6. Find readings within a pressure range
SELECT * FROM compressor_data WHERE Pressure_bar BETWEEN 6.5 AND 7.0 ORDER BY Power_kW DESC LIMIT 20;


-- 7. Analyze selected compressors
SELECT * FROM compressor_data WHERE Compressor_ID IN ('CP-01', 'CP-03', 'CP-05') ORDER BY Power_kW DESC LIMIT 20;


-- 8. Find compressors that were not stopped
SELECT * FROM compressor_data WHERE NOT Running_Status = 'Stopped' ORDER BY Timestamp;





-- ============================================================
-- AGGREGATION & KPI ANALYSIS
-- ============================================================

-- Average power by compressor

SELECT
    Compressor_ID,
    AVG(Power_kW) AS Average_Power_kW
FROM compressor_data
GROUP BY Compressor_ID;


-- Compressor KPI summary

SELECT
    Compressor_ID,
    COUNT(*) AS Total_Readings,
    AVG(Power_kW) AS Average_Power_kW,
    MIN(Power_kW) AS Minimum_Power_kW,
    MAX(Power_kW) AS Maximum_Power_kW,
    AVG(Current_A) AS Average_Current_A,
    AVG(Flow_m3h) AS Average_Flow_m3h,
    AVG(Pressure_bar) AS Average_Pressure_bar,
    AVG(Load_Percent) AS Average_Load_Percent
FROM compressor_data
GROUP BY Compressor_ID
ORDER BY Average_Power_kW DESC;


-- Compressors with average power above 25 kW

SELECT
    Compressor_ID,
    AVG(Power_kW) AS Average_Power_kW
FROM compressor_data
GROUP BY Compressor_ID
HAVING AVG(Power_kW) > 25
ORDER BY Average_Power_kW DESC;


-- Running readings by compressor

SELECT
    Compressor_ID,
    COUNT(*) AS Running_Readings
FROM compressor_data
WHERE Running_Status = 'Running'
GROUP BY Compressor_ID
ORDER BY Running_Readings DESC;


-- Average power during running conditions

SELECT
    Compressor_ID,
    AVG(Power_kW) AS Average_Running_Power_kW
FROM compressor_data
WHERE Running_Status = 'Running'
GROUP BY Compressor_ID
ORDER BY Average_Running_Power_kW DESC;