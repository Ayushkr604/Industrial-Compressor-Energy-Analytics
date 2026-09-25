-- ============================================================
-- Industrial Compressor Energy Analytics
-- SQL Analysis - Time Series
-- ============================================================


-- Daily average compressor performance

SELECT
    date(Timestamp) AS Reading_Date,
    ROUND(AVG(Power_kW), 2) AS Average_Power_kW,
    ROUND(AVG(Flow_m3h), 2) AS Average_Flow_m3h,
    ROUND(AVG(Load_Percent), 2) AS Average_Load_Percent
FROM compressor_data
GROUP BY date(Timestamp)
ORDER BY Reading_Date;


-- Daily performance by compressor

SELECT
    date(Timestamp) AS Reading_Date,
    Compressor_ID,
    ROUND(AVG(Power_kW), 2) AS Average_Power_kW,
    ROUND(AVG(Flow_m3h), 2) AS Average_Flow_m3h,
    ROUND(AVG(Load_Percent), 2) AS Average_Load_Percent
FROM compressor_data
GROUP BY date(Timestamp), Compressor_ID
ORDER BY Reading_Date, Compressor_ID;


-- Monthly compressor performance

SELECT
    strftime('%Y-%m', Timestamp) AS Month,
    Compressor_ID,
    ROUND(AVG(Power_kW), 2) AS Average_Power_kW,
    ROUND(AVG(Flow_m3h), 2) AS Average_Flow_m3h,
    ROUND(AVG(Load_Percent), 2) AS Average_Load_Percent
FROM compressor_data
GROUP BY Month, Compressor_ID
ORDER BY Month, Compressor_ID;


-- Top 10 highest-power days

SELECT
    date(Timestamp) AS Reading_Date,
    ROUND(AVG(Power_kW), 2) AS Average_Power_kW
FROM compressor_data
GROUP BY date(Timestamp)
ORDER BY Average_Power_kW DESC
LIMIT 10;
