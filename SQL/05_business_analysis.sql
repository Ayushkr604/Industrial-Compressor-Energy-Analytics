-- ============================================================
-- Industrial Compressor Energy Analytics
-- SQL Analysis - Business Analysis
-- ============================================================

-- 1. Average power consumption by compressor
SELECT
    Compressor_ID,
    ROUND(AVG(Power_kW), 2) AS Average_Power_kW
FROM cleaned_compressor_data
GROUP BY Compressor_ID
ORDER BY Average_Power_kW DESC;


-- 2. Average power when compressors are running
SELECT
    Compressor_ID,
    COUNT(*) AS Running_Readings,
    ROUND(AVG(Power_kW), 2) AS Average_Running_Power_kW
FROM cleaned_compressor_data
WHERE Running_Status = 'Running'
GROUP BY Compressor_ID
ORDER BY Average_Running_Power_kW DESC;


-- 3. Power consumption by load category
SELECT
    CASE
        WHEN Load_Percent < 50 THEN 'Low Load'
        WHEN Load_Percent < 80 THEN 'Medium Load'
        ELSE 'High Load'
    END AS Load_Category,
    COUNT(*) AS Reading_Count,
    ROUND(AVG(Power_kW), 2) AS Average_Power_kW
FROM cleaned_compressor_data
GROUP BY Load_Category
ORDER BY Average_Power_kW DESC;


-- 4. Power consumption relative to airflow
SELECT
    Compressor_ID,
    ROUND(AVG(Power_kW), 2) AS Average_Power_kW,
    ROUND(AVG(Flow_m3h), 2) AS Average_Flow_m3h,
    ROUND(
        AVG(Power_kW) / AVG(Flow_m3h) * 100,
        3
    ) AS Power_per_100m3h
FROM cleaned_compressor_data
GROUP BY Compressor_ID
ORDER BY Power_per_100m3h DESC;


-- 5. Maximum power reached by each compressor
SELECT
    Compressor_ID,
    ROUND(MAX(Power_kW), 2) AS Maximum_Power_kW
FROM cleaned_compressor_data
GROUP BY Compressor_ID
ORDER BY Maximum_Power_kW DESC;


-- 6. Average power during high-load operation
SELECT
    Compressor_ID,
    COUNT(*) AS High_Load_Readings,
    ROUND(AVG(Power_kW), 2) AS Average_High_Load_Power_kW
FROM cleaned_compressor_data
WHERE Load_Percent >= 80
GROUP BY Compressor_ID
ORDER BY Average_High_Load_Power_kW DESC;


-- 7. Average airflow during high-load operation
SELECT
    Compressor_ID,
    ROUND(AVG(Flow_m3h), 2) AS Average_High_Load_Flow_m3h,
    ROUND(AVG(Power_kW), 2) AS Average_High_Load_Power_kW
FROM cleaned_compressor_data
WHERE Load_Percent >= 80
GROUP BY Compressor_ID
ORDER BY Average_High_Load_Power_kW DESC;


-- 7. Average airflow during high-load operation
SELECT
    Compressor_ID,
    ROUND(AVG(Flow_m3h), 2) AS Average_High_Load_Flow_m3h,
    ROUND(AVG(Power_kW), 2) AS Average_High_Load_Power_kW
FROM cleaned_compressor_data
WHERE Load_Percent >= 80
GROUP BY Compressor_ID
ORDER BY Average_High_Load_Power_kW DESC;


-- 8. Compressor contribution to total power consumption
SELECT
    Compressor_ID,
    ROUND(SUM(Power_kW), 2) AS Total_Power_kW,
    ROUND(
        SUM(Power_kW) * 100.0 /
        (SELECT SUM(Power_kW) FROM cleaned_compressor_data),
        2
    ) AS Power_Contribution_Percent
FROM cleaned_compressor_data
GROUP BY Compressor_ID
ORDER BY Power_Contribution_Percent DESC;


-- 9. Monthly compressor power consumption
SELECT
    strftime('%Y-%m', Timestamp) AS Month,
    Compressor_ID,
    ROUND(AVG(Power_kW), 2) AS Average_Power_kW,
    ROUND(AVG(Flow_m3h), 2) AS Average_Flow_m3h,
    ROUND(AVG(Load_Percent), 2) AS Average_Load_Percent
FROM cleaned_compressor_data
GROUP BY Month, Compressor_ID
ORDER BY Month, Compressor_ID;


-- 10. Top 10 highest-power days
SELECT
    date(Timestamp) AS Reading_Date,
    ROUND(AVG(Power_kW), 2) AS Average_Power_kW,
    ROUND(AVG(Load_Percent), 2) AS Average_Load_Percent
FROM cleaned_compressor_data
GROUP BY date(Timestamp)
ORDER BY Average_Power_kW DESC
LIMIT 10;


-- 11. Daily power consumption by compressor
SELECT
    date(Timestamp) AS Reading_Date,
    Compressor_ID,
    ROUND(AVG(Power_kW), 2) AS Average_Power_kW,
    ROUND(AVG(Flow_m3h), 2) AS Average_Flow_m3h
FROM cleaned_compressor_data
GROUP BY date(Timestamp), Compressor_ID
ORDER BY Reading_Date, Compressor_ID;


-- 12. Compressor power-to-flow efficiency
SELECT
    Compressor_ID,
    ROUND(
        SUM(Power_kW) / SUM(Flow_m3h) * 100,
        3
    ) AS kW_per_100m3h
FROM cleaned_compressor_data
GROUP BY Compressor_ID
ORDER BY kW_per_100m3h;


-- 13. High-power readings during high-load operation
SELECT
    Compressor_ID,
    COUNT(*) AS High_Power_High_Load_Readings,
    ROUND(AVG(Power_kW), 2) AS Average_Power_kW,
    ROUND(AVG(Load_Percent), 2) AS Average_Load_Percent
FROM cleaned_compressor_data
WHERE Power_kW > 30
  AND Load_Percent >= 80
GROUP BY Compressor_ID
ORDER BY High_Power_High_Load_Readings DESC;


-- 13. High-power readings during high-load operation
SELECT
    Compressor_ID,
    COUNT(*) AS High_Power_High_Load_Readings,
    ROUND(AVG(Power_kW), 2) AS Average_Power_kW,
    ROUND(AVG(Load_Percent), 2) AS Average_Load_Percent
FROM cleaned_compressor_data
WHERE Power_kW > 30
  AND Load_Percent >= 80
GROUP BY Compressor_ID
ORDER BY High_Power_High_Load_Readings DESC;


