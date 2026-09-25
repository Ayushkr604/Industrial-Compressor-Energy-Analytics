-- ============================================================
-- Industrial Compressor Energy Analytics
-- SQL Analysis - JOINs
-- ============================================================


-- INNER JOIN: combine compressor readings with master data

SELECT
    c.Compressor_ID,
    c.Power_kW,
    c.Flow_m3h,
    m.Compressor_Type,
    m.Rated_Power_kW,
    m.Location
FROM compressor_data AS c
JOIN compressor_master AS m
    ON c.Compressor_ID = m.Compressor_ID
LIMIT 10;


-- Compressor performance using master data

SELECT
    m.Compressor_ID,
    m.Location,
    m.Compressor_Type,
    m.Rated_Power_kW,
    ROUND(AVG(c.Power_kW), 2) AS Average_Power_kW,
    ROUND(AVG(c.Load_Percent), 2) AS Average_Load_Percent
FROM compressor_data AS c
JOIN compressor_master AS m
    ON c.Compressor_ID = m.Compressor_ID
GROUP BY
    m.Compressor_ID,
    m.Location,
    m.Compressor_Type,
    m.Rated_Power_kW
ORDER BY Average_Power_kW DESC;


-- LEFT JOIN: check reading coverage for every compressor

SELECT
    m.Compressor_ID,
    m.Location,
    COUNT(c.Compressor_ID) AS Reading_Count
FROM compressor_master AS m
LEFT JOIN compressor_data AS c
    ON m.Compressor_ID = c.Compressor_ID
GROUP BY
    m.Compressor_ID,
    m.Location
ORDER BY Reading_Count DESC;
