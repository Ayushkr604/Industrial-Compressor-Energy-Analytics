# Industrial Compressor Energy Analytics

> End-to-end Data Analytics project for analyzing industrial compressor performance, energy consumption, operating behavior, and sensor data quality.

---

## 📌 Overview

Industrial compressors are significant energy-consuming assets in process industries. Monitoring their power consumption, airflow, load, pressure, temperature, and current can help identify changes in operating behavior and potential opportunities for energy optimization.

This project demonstrates an end-to-end Data Analytics workflow using a synthetic industrial compressor dataset.

The project currently covers:

- Data quality assessment
- Data cleaning
- Exploratory Data Analysis
- KPI analysis
- Time-series analysis
- SQL-based business analysis
- Compressor performance comparison
- Energy-efficiency analysis
- Statistical outlier detection
- Window-function analysis
- Business-oriented analytical queries

Future phases will extend the project into Python-based EDA, visualization, Power BI dashboards, statistical analysis, and predictive analytics.

> **Important:** The dataset used in this repository is fully synthetic and created for portfolio and learning purposes. It does not contain confidential, proprietary, or real industrial plant data.

---

# 🎯 Business Problem

Industrial compressors operate under changing load, flow, pressure, temperature, and operating conditions.

Understanding these variables together can help answer questions such as:

- Which compressors consume the most power?
- Which compressors operate at higher loads?
- How does power consumption change with airflow?
- Which compressors show higher power consumption relative to airflow?
- How does compressor performance change over time?
- Are there missing or duplicate sensor readings?
- Which readings appear statistically unusual?
- What operating patterns could be useful for future anomaly detection?
- Which variables could be useful for future predictive-maintenance models?

---

# 🎯 Project Objectives

The main objectives of this project are to:

- Clean and validate compressor sensor data
- Identify missing values and duplicate records
- Detect and flag statistical outliers
- Calculate compressor-wise performance KPIs
- Analyze power, flow, pressure, current, temperature, and load
- Perform time-series analysis
- Compare compressor operating behavior
- Calculate energy-efficiency indicators
- Use SQL for business-oriented analysis
- Build reproducible analytical workflows
- Communicate findings through visualizations and dashboards
- Prepare the project for future predictive analytics

---

# 📊 Dataset

The project uses a synthetic dataset representing hourly operating measurements from five industrial compressors.

| Feature | Description |
|---|---|
| Timestamp | Date and time of the reading |
| Compressor_ID | Unique compressor identifier |
| Running_Status | Compressor operating status |
| Current_A | Motor current in amperes |
| Power_kW | Electrical power consumption |
| Pressure_bar | Discharge pressure |
| Flow_m3h | Airflow rate |
| Temperature_C | Operating temperature |
| Load_Percent | Compressor load percentage |

## Dataset Summary

| Metric | Value |
|---|---:|
| Time period | January–March 2026 |
| Raw records | 10,830 |
| Compressors | 5 |
| Data frequency | Hourly |
| Dataset type | Synthetic |

---

# 🔍 Data Quality & Cleaning

The raw dataset was intentionally created with data-quality issues to simulate common industrial sensor-data problems.

The analysis includes:

- Duplicate-record detection
- Missing-value identification
- Invalid-value checks
- Statistical outlier detection
- Compressor coverage checks
- Sensor-value validation

## Cleaning Results

- **10,830** raw records were loaded.
- **30 duplicate records** were identified and removed during the Excel cleaning workflow.
- Missing sensor values were identified and handled during cleaning.
- Statistical outliers were flagged rather than automatically removed.
- Outlier handling was treated as an investigation step because unusual industrial readings may represent genuine operating events.

---

# 📈 Key Performance Indicators

The project calculates compressor-level KPIs including:

- Average Power (kW)
- Average Current (A)
- Average Flow (m³/h)
- Average Pressure (bar)
- Average Load (%)
- Maximum Power (kW)
- Power per 100 m³ of airflow
- High-load operating readings
- Daily and monthly performance metrics

---

# ⚙️ Key Analytical Findings

Based on the current analysis of the synthetic dataset:

## Compressor Power

| Compressor | Avg Power |
|---|---:|
| CP-05 | 27.06 kW |
| CP-03 | 25.43 kW |
| CP-01 | 23.57 kW |
| CP-02 | 22.12 kW |
| CP-04 | 20.58 kW |

CP-05 has the highest average power consumption in the synthetic dataset, while CP-04 has the lowest.

## Power vs Flow

The project found a strong positive relationship between power consumption and airflow.

**Power vs. Flow correlation: ~0.918**

This indicates that higher airflow observations in the synthetic dataset are generally associated with higher power consumption.

## Power per 100 m³

| Compressor | Power / 100 m³ |
|---|---:|
| CP-05 | 7.29 |
| CP-03 | 7.13 |
| CP-01 | 7.04 |
| CP-04 | 6.99 |
| CP-02 | 6.97 |

This metric provides an additional way to compare power consumption relative to airflow.

## Load Behavior

High-load readings were defined as observations where:

`Load_Percent > 75`

| Compressor | High-load readings |
|---|---:|
| CP-05 | 1,283 |
| CP-03 | 925 |
| CP-01 | 532 |
| CP-02 | 209 |
| CP-04 | 20 |

These values help characterize differences in operating-load patterns between compressors.

> All results above are derived from synthetic portfolio data.

---

# 🧮 SQL Analysis

SQL is being used as a major analytical component of the project.

The SQL workflow currently covers:

## Basic Analysis

- `SELECT`
- `WHERE`
- `ORDER BY`
- `LIMIT`
- `AND` / `OR` / `NOT`
- `BETWEEN`
- `IN`
- `IS NULL`
- Aggregate functions

## Aggregation

- `GROUP BY`
- `HAVING`
- `COUNT`
- `SUM`
- `AVG`
- `MAX`
- Conditional aggregation

## Business Analysis

- Compressor-wise KPIs
- Load analysis
- Power-to-flow efficiency
- High-load analysis
- High-power readings
- Daily performance
- Monthly performance
- Compressor contribution analysis

## Joins

- `INNER JOIN`
- `LEFT JOIN`
- Compressor master-data integration

## Subqueries & CTEs

- Analytical subqueries
- Common Table Expressions (`WITH`)

## Window Functions

- `ROW_NUMBER()`
- `RANK()`
- `LAG()`
- Partitioned ranking
- Top-N analysis by compressor
- Hour-to-hour power-change analysis

## SQL Utility Functions

- `CASE`
- `COALESCE()`
- `NULLIF()`

These techniques are used to transform raw sensor readings into business-oriented performance metrics.

---

# 🕒 Time-Series Analysis

The SQL analysis includes:

- Daily average power
- Daily average flow
- Daily average load
- Compressor-wise daily performance
- Monthly compressor performance
- Highest-power days
- Hour-to-hour power changes
- Sudden power-change detection

Window functions such as `LAG()` are used to compare a reading with the previous reading for the same compressor.

This allows the analysis to identify large changes in compressor power between consecutive observations.

---

# 📊 Excel Analysis

The Excel workbook contains:

- Raw data
- Data-quality checks
- Data cleaning
- Missing-value handling
- Duplicate detection
- Outlier analysis
- Compressor-wise KPI analysis
- Exploratory Data Analysis
- Time-series analysis
- Dashboard
- Business insights

Main workbook:

`EXCEL/Compressor_Analysis.xlsx`

---

# 🐍 Python Analysis

Python will extend the project beyond Excel and SQL.

Planned analysis includes:

- Pandas-based data loading
- Data preprocessing
- Data cleaning
- Exploratory Data Analysis
- Statistical analysis
- Correlation analysis
- Feature engineering
- Matplotlib visualizations
- Advanced EDA
- Future anomaly detection
- Future predictive modelling

Python scripts will be added to:

`PYTHON/`

---

# 📊 Power BI

A future Power BI phase will convert the analytical results into an interactive business dashboard.

Planned components include:

- KPI cards
- Compressor comparison
- Power trends
- Flow trends
- Load analysis
- Efficiency comparison
- Interactive filters
- Compressor-level drilldowns

Power BI files will be added to:

`POWERBI/`

---

# 🔮 Future Machine Learning Applications

The analytical foundation can later be extended into predictive analytics.

Potential applications include:

## Anomaly Detection

Detect when a compressor's:

- Power
- Current
- Pressure
- Temperature
- Flow
- Specific efficiency

starts deviating significantly from its normal operating range.

## Predictive Analytics

Future models could investigate:

- Compressor performance degradation
- Abnormal operating conditions
- Energy-efficiency deterioration
- Sensor anomalies
- Operating-state classification

Tree-based machine-learning models may be evaluated in a future phase.

---

# 🗂️ Project Structure

```text
Industrial-Compressor-Energy-Analytics/
│
├── DATA/
│   ├── RAW/
│   │   └── synthetic_compressor_data_raw.csv
│   │
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
│   ├── 03_joins.sql
│   ├── 04_data_cleaning.sql
│   └── 05_business_analysis.sql
│
├── .gitignore
└── README.md


---

# 🛠️ Tools & Technologies

| Tool | Purpose |
|---|---|
| Microsoft Excel | Data cleaning, KPI analysis, EDA and dashboarding |
| SQLite | SQL analysis and database querying |
| SQL | Data exploration, aggregation, joins and business analysis |
| Python | Data analysis, visualization and future ML |
| Pandas | Data manipulation and preprocessing |
| Matplotlib | Data visualization |
| Power BI | Interactive dashboarding |
| Git | Version control |
| GitHub | Portfolio and project documentation |

---

# 💡 Business Insights

The current analysis demonstrates how raw industrial sensor data can be converted into actionable analytical metrics.

Key analytical themes include:

1. **Compressor comparison**  
   Compressor-level KPIs reveal differences in power consumption, airflow, and load behavior.

2. **Energy efficiency**  
   Power-per-flow metrics provide an additional perspective beyond absolute power consumption.

3. **Operating load**  
   High-load reading counts help identify differences in operating behavior.

4. **Time-series behavior**  
   Daily, monthly, and hour-to-hour analysis can reveal changes in operating patterns.

5. **Data quality**  
   Duplicate, missing, and statistically unusual readings need to be assessed before building reliable analytical or machine-learning models.

6. **Future predictive analytics**  
   Historical operating behavior provides a foundation for future anomaly-detection and predictive-maintenance workflows.

---

# 🚀 Project Status

## Completed

- [x] Synthetic dataset creation
- [x] Data dictionary
- [x] Excel data cleaning
- [x] Excel KPI analysis
- [x] Excel EDA
- [x] Excel dashboard
- [x] SQL database creation
- [x] SQL basic analysis
- [x] SQL time-series analysis
- [x] SQL joins
- [x] SQL data-quality analysis
- [x] SQL business analysis
- [x] SQL window-function analysis
- [x] SQL efficiency analysis

## Upcoming

- [ ] Complete advanced SQL checkpoint
- [ ] Python + Pandas analysis
- [ ] Python EDA
- [ ] Python visualizations
- [ ] Statistical analysis
- [ ] Power BI dashboard
- [ ] Final business insights
- [ ] Portfolio report
- [ ] Future anomaly-detection model

---

# 📚 Learning Outcomes

This project demonstrates practical experience with:

- Data cleaning
- Exploratory Data Analysis
- KPI development
- SQL analytics
- Relational data analysis
- Time-series analysis
- Window functions
- Business-oriented metrics
- Data visualization
- Analytical storytelling
- Git/GitHub workflow

The project is designed to demonstrate the complete progression from:

**Raw sensor data → Cleaned data → Analysis → Business insights → Visualization → Future predictive analytics**

---

# ⚠️ Disclaimer

## Synthetic Dataset

This repository uses **synthetic data created specifically for portfolio and educational purposes**.

The dataset does not represent actual plant measurements and does not contain confidential, proprietary, or restricted industrial information.

The project demonstrates analytical methods and workflow rather than reporting real industrial performance.

---

# 👤 Author

## Ayush Kumar

**Computer Science Engineering**  
**BITS Pilani**