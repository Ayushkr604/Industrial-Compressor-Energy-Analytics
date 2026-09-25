# Industrial Compressor Energy Analytics

## Overview

This project analyzes industrial compressor data to identify energy consumption patterns, operating behavior, data-quality issues, and potential opportunities for energy optimization.

The project follows an end-to-end Data Analytics workflow covering data cleaning, exploratory data analysis, KPI analysis, SQL analysis, visualization, dashboarding, and future machine-learning applications.

> **Note:** The dataset used in this repository is synthetic and created for portfolio and learning purposes. It does not contain confidential or proprietary industrial data.

---

## Business Problem

Industrial compressors are major energy-consuming assets in process industries. Changes in operating conditions can affect power consumption, efficiency, and overall equipment performance.

The key business questions addressed in this project are:

- Which compressors consume the most power?
- How does power consumption change with airflow and load?
- Which operating conditions are associated with higher energy consumption?
- Are there missing, duplicate, or anomalous sensor readings?
- How does compressor performance change over time?
- Which variables could be useful for future predictive-maintenance or anomaly-detection models?

---

## Objectives

- Clean and validate industrial compressor sensor data.
- Identify missing values, duplicate records, and statistical outliers.
- Calculate compressor-wise performance KPIs.
- Analyze relationships between power, flow, pressure, current, temperature, and load.
- Perform time-series analysis of compressor performance.
- Use SQL for filtering, aggregation, KPI analysis, and joins.
- Build Excel-based analysis and dashboards.
- Develop visualizations for communicating operational insights.
- Prepare the analytical workflow for future machine-learning models.

---

## Dataset

The project uses a synthetic compressor dataset representing hourly operating data for five compressors.

| Feature | Description |
|---|---|
| Timestamp | Date and time of the reading |
| Compressor_ID | Unique compressor identifier |
| Running_Status | Compressor operating status |
| Current_A | Motor current in amperes |
| Power_kW | Electrical power consumption |
| Pressure_bar | Discharge pressure |
| Flow_m3h | Air flow rate |
| Temperature_C | Operating temperature |
| Load_Percent | Compressor load percentage |

### Dataset Summary

- **Time period:** January–March 2026
- **Raw records:** 10,830
- **Compressors:** 5
- **Data frequency:** Hourly
- **Dataset type:** Synthetic

---

## Methodology

The project follows the following analytical workflow:

1. Data Collection
2. Data Quality Assessment
3. Data Cleaning
4. Exploratory Data Analysis
5. KPI Analysis
6. Time-Series Analysis
7. SQL Analysis
8. Visualization & Dashboarding
9. Business Insights
10. Future Predictive Analytics

---

## Tools & Technologies

- **Microsoft Excel** – Data cleaning, KPI calculations, EDA and dashboarding
- **SQL / SQLite** – Data querying, aggregation, filtering and joins
- **Python** – Data analysis and future machine-learning workflows
- **Power BI** – Interactive dashboard development
- **Git & GitHub** – Version control and project documentation

---

## Excel Analysis

The Excel workbook contains:

- Raw data
- Data quality checks
- Data cleaning
- Missing-value handling
- Duplicate detection
- Outlier analysis
- Compressor-wise KPI analysis
- Exploratory data analysis
- Time-series analysis
- Dashboard and insights

The main workbook is available in:

`EXCEL/Compressor_Analysis.xlsx`

---

## SQL Analysis

SQL analysis is performed using SQLite.

The SQL workflow includes:

- Basic data exploration
- Filtering and sorting
- Aggregate functions
- GROUP BY and HAVING
- CASE statements
- Date and time analysis
- Compressor-wise KPI analysis
- Time-series analysis
- INNER JOIN
- LEFT JOIN

SQL scripts are available in:

`SQL/`

---

## Python Analysis

Python will be used for:

- Data preprocessing
- Exploratory data analysis
- Statistical analysis
- Visualization
- Feature engineering
- Future anomaly detection
- Future predictive modelling

Python analysis files will be added to:

`PYTHON/`

---

## Project Structure

```text
Industrial-Compressor-Energy-Analytics/
│
├── DATA/
│   ├── RAW/
│   │   └── synthetic_compressor_data_raw.csv
│   └── REFERENCE/
│       └── compressor_data_dictionary.xlsx
│
├── DOCS/
│
├── EXCEL/
│   └── Compressor_Analysis.xlsx
│
├── POWERBI/
│
├── PYTHON/
│
├── REPORTS/
│
├── SQL/
│   ├── 01_basic_analysis.sql
│   ├── 02_time_series_analysis.sql
│   └── 03_joins.sql
│
├── .gitignore
└── README.md
