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