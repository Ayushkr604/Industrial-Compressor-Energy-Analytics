-- ============================================================
-- Industrial Compressor Energy Analytics
-- SQL Analysis - Data Cleaning
-- ============================================================

-- Find duplicate records
SELECT
    Timestamp,
    Compressor_ID,
    Running_Status,
    Current_A,
    Power_kW,
    Pressure_bar,
    Flow_m3h,
    Temperature_C,
    Load_Percent,
    COUNT(*) AS Duplicate_Count
FROM compressor_data
GROUP BY
    Timestamp,
    Compressor_ID,
    Running_Status,
    Current_A,
    Power_kW,
    Pressure_bar,
    Flow_m3h,
    Temperature_C,
    Load_Percent
HAVING COUNT(*) > 1
ORDER BY Duplicate_Count DESC;


-- Check missing values
SELECT
    COUNT(*) AS Total_Rows,
    SUM(CASE WHEN Current_A IS NULL THEN 1 ELSE 0 END) AS Missing_Current,
    SUM(CASE WHEN Power_kW IS NULL THEN 1 ELSE 0 END) AS Missing_Power,
    SUM(CASE WHEN Pressure_bar IS NULL THEN 1 ELSE 0 END) AS Missing_Pressure,
    SUM(CASE WHEN Flow_m3h IS NULL THEN 1 ELSE 0 END) AS Missing_Flow,
    SUM(CASE WHEN Temperature_C IS NULL THEN 1 ELSE 0 END) AS Missing_Temperature,
    SUM(CASE WHEN Load_Percent IS NULL THEN 1 ELSE 0 END) AS Missing_Load
FROM compressor_data;


-- Check invalid pressure values
SELECT
    COUNT(*) AS Invalid_Pressure_Readings
FROM compressor_data
WHERE Pressure_bar < 0;


-- Check invalid flow values
SELECT
    COUNT(*) AS Invalid_Flow_Readings
FROM compressor_data
WHERE Flow_m3h < 0;


-- Check invalid power values
SELECT
    COUNT(*) AS Invalid_Power_Readings
FROM compressor_data
WHERE Power_kW < 0;


-- Check invalid load values
SELECT
    COUNT(*) AS Invalid_Load_Readings
FROM compressor_data
WHERE Load_Percent < 0
   OR Load_Percent > 100;


-- Check compressor IDs
SELECT
    Compressor_ID,
    COUNT(*) AS Reading_Count
FROM compressor_data
GROUP BY Compressor_ID
ORDER BY Compressor_ID;


-- Identify high-power readings
SELECT
    COUNT(*) AS High_Power_Readings
FROM compressor_data
WHERE Power_kW > 30;


-- Identify high-current readings
SELECT
    COUNT(*) AS High_Current_Readings
FROM compressor_data
WHERE Current_A > 60;


-- Identify high-temperature readings
SELECT
    COUNT(*) AS High_Temperature_Readings
FROM compressor_data
WHERE Temperature_C > 50;


-- Top 10 highest-power readings
SELECT
    Timestamp,
    Compressor_ID,
    Power_kW,
    Current_A,
    Flow_m3h,
    Load_Percent
FROM compressor_data
ORDER BY Power_kW DESC
LIMIT 10;


-- Top 10 highest-current readings
SELECT
    Timestamp,
    Compressor_ID,
    Current_A,
    Power_kW,
    Load_Percent
FROM compressor_data
ORDER BY Current_A DESC
LIMIT 10;



-- Create a cleaned analytical view
CREATE VIEW IF NOT EXISTS cleaned_compressor_data AS
SELECT
    Timestamp,
    Compressor_ID,
    Running_Status,
    Current_A,
    Power_kW,
    Pressure_bar,
    Flow_m3h,
    Temperature_C,
    Load_Percent
FROM compressor_data
WHERE Power_kW >= 0
  AND Current_A >= 0
  AND Pressure_bar >= 0
  AND Flow_m3h >= 0
  AND Temperature_C >= 0
  AND Load_Percent BETWEEN 0 AND 100;


  -- Check cleaned record count
SELECT
    COUNT(*) AS Cleaned_Records
FROM cleaned_compressor_data;


-- Compressor-wise KPIs from cleaned data
SELECT
    Compressor_ID,
    COUNT(*) AS Reading_Count,
    ROUND(AVG(Power_kW), 2) AS Avg_Power_kW,
    ROUND(AVG(Current_A), 2) AS Avg_Current_A,
    ROUND(AVG(Flow_m3h), 2) AS Avg_Flow_m3h,
    ROUND(AVG(Pressure_bar), 2) AS Avg_Pressure_bar,
    ROUND(AVG(Load_Percent), 2) AS Avg_Load_Percent
FROM cleaned_compressor_data
GROUP BY Compressor_ID
ORDER BY Avg_Power_kW DESC;


