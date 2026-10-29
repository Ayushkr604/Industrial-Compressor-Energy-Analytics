# Industrial Compressor Energy Analytics

**An end-to-end Data Analytics project exploring industrial compressor performance, energy consumption, operating behaviour, and sensor data quality using Python, SQL, and Excel.**

> **Disclaimer:** This project uses entirely synthetic data for educational and portfolio purposes. It does not contain actual industrial plant measurements and does not claim verified energy savings.

---

## 1. Project Overview

Industrial compressors are important energy-consuming assets in process industries. Analysing their power consumption, airflow, pressure, temperature, current, and operating load can help identify patterns and potential areas for further investigation.

This project demonstrates how raw sensor-style data can be transformed into structured datasets, analytical metrics, visualisations, and business-oriented insights.

### Business Questions

- Which compressors have the highest average power consumption?
- How does power consumption relate to airflow?
- How do operating load and compressor status vary?
- Which sensor readings are missing or statistically unusual?
- How does compressor behaviour change over time?
- Which operating patterns deserve further investigation?
- How can the analysis support future dashboards and anomaly detection?

## 2. Project Objectives

- Assess and improve data quality.
- Identify duplicate records and missing sensor values.
- Investigate statistical outliers.
- Calculate compressor-level performance indicators.
- Analyse power, current, pressure, airflow, temperature, and load.
- Perform time-series and correlation analysis.
- Use SQL to answer business-oriented questions.
- Build reproducible Python analysis workflows.
- Prepare data for interactive Power BI reporting.
- Develop evidence-based recommendations while acknowledging analytical limitations.

## 3. Dataset Description

The project uses a synthetic dataset representing hourly measurements from five fictional industrial compressors.

| Column | Description |
|---|---|
| `Timestamp` | Date and time of each observation |
| `Compressor_ID` | Compressor identifier |
| `Running_Status` | Running or stopped status |
| `Current_A` | Motor current in amperes |
| `Power_kW` | Electrical power in kilowatts |
| `Pressure_bar` | Pressure reading in bar |
| `Flow_m3h` | Airflow in cubic metres per hour |
| `Temperature_C` | Temperature in degrees Celsius |
| `Load_Percent` | Compressor load percentage |

### Dataset Summary

| Metric | Value |
|---|---:|
| Observation period | January–March 2026 |
| Raw records | 10,830 |
| Cleaned records | 10,800 |
| Number of compressors | 5 |
| Sampling frequency | Hourly |
| Dataset type | Synthetic |

The cleaned dataset is stored in:

`DATA/CLEANED/compressor_data_cleaned.csv`

The cleaned dataset contains 10,800 records. It preserves 30 missing readings each in pressure, airflow, and temperature for transparent data-quality analysis.

## 4. Tools and Technologies

| Technology | Purpose |
|---|---|
| Python | Data analysis and automation |
| Pandas | Data manipulation and cleaning |
| Matplotlib | Data visualisation |
| SQL | Data querying and business analysis |
| SQLite | Local analytical database |
| Microsoft Excel | Data preparation, KPI analysis, and spreadsheet-based EDA |
| Power BI | Interactive dashboard development |
| Git | Version control |
| GitHub | Project hosting and documentation |

## 5. Project Workflow

The project follows an end-to-end analytical workflow.

1. **Data inspection:** Review dataset structure, timestamps, sensor fields, and compressor coverage.
2. **Data cleaning:** Identify duplicate records and validate sensor values.
3. **Missing-value analysis:** Quantify missing readings and investigate appropriate handling methods.
4. **Outlier analysis:** Identify statistically unusual readings for further investigation.
5. **Exploratory Data Analysis:** Compare compressor performance and examine relationships between variables.
6. **SQL analysis:** Use aggregations, joins, subqueries, CTEs, and window functions to investigate business questions.
7. **Visualisation:** Generate charts and summary tables.
8. **Power BI preparation:** Create a dashboard-ready dataset.
9. **Future development:** Build an interactive dashboard and investigate possible anomaly-detection applications.

## 6. Key Analytical Findings

The following findings are based on the current Python analysis of the synthetic dataset.

### 6.1 Compressor Power Comparison

Average power consumption was calculated using observations where the compressor status was `Running`.

| Compressor | Running Readings | Average Power |
|---|---:|---:|
| CP-05 | 2,019 | 28.07 kW |
| CP-03 | 2,038 | 26.22 kW |
| CP-01 | 2,023 | 24.37 kW |
| CP-02 | 2,036 | 22.79 kW |
| CP-04 | 2,042 | 21.12 kW |

**Finding:** CP-05 has the highest average running power, while CP-04 has the lowest.

**Business interpretation:** This comparison identifies differences in power consumption. It does not establish which compressor is most or least efficient because the compressors may operate under different airflow, pressure, and load conditions.

### 6.2 Relationship Between Power and Airflow

The running-only correlation between power consumption and airflow is approximately **0.851**.

**Finding:** Higher airflow readings are generally associated with higher power consumption in the synthetic dataset.

**Business interpretation:** Airflow is an important variable to consider when analysing compressor power. Correlation alone does not establish causation or prove energy efficiency.

### 6.3 Operating Status

The dataset contains:

- **10,158 running observations**
- **642 stopped observations**

Operating-status analysis helps compare how frequently each compressor is recorded as running or stopped.

These observations represent hourly records, not independently verified equipment operating logs.

### 6.4 Data Quality

The Python analysis identified:

- 10,800 cleaned records.
- No duplicate rows in the cleaned dataset.
- 30 missing pressure readings.
- 30 missing airflow readings.
- 30 missing temperature readings.
- Statistically unusual temperature readings requiring investigation.

Outliers are flagged for review rather than automatically classified as equipment faults.

### 6.5 Estimated Energy Consumption

The project calculates estimated energy summaries by treating each hourly power observation as representing one hour.

These calculations are estimates derived from synthetic data, not verified meter readings. They should not be interpreted as actual plant energy consumption or measured energy savings.

## 7. Python Analysis

Python scripts are organised in the `PYTHON/` directory.

| Script | Purpose |
|---|---|
| `01_python_setup.py` | Initial setup and dataset inspection |
| `02_python_fundamentals.py` | Python fundamentals |
| `03_pandas_basics.py` | Pandas operations |
| `04_data_quality_and_cleaning.py` | Data-quality checks and cleaning |
| `05_missing_values_and_imputation.py` | Missing-value analysis |
| `06_outlier_analysis.py` | Statistical outlier analysis |
| `07_exploratory_data_analysis.py` | EDA, summary tables, and charts |
| `08_sync_sql_database.py` | Synchronise the local SQL database with the cleaned CSV |

### Python Visualisations

Generated charts are stored in `OUTPUT/EDA/charts/`.

Current visualisations include:

- `running_power_comparison.png`
- `monthly_running_power.png`
- `average_running_temperature.png`
- `sensor_correlation_matrix.png`

Summary tables are available as CSV files under `OUTPUT/EDA/`.

## 8. SQL Analysis

The SQL scripts are stored in the `SQL/` directory.

The analysis covers:

- Data filtering and sorting.
- Aggregate functions and conditional aggregation.
- Compressor-level KPIs.
- Data cleaning and quality checks.
- Joins and compressor master-data integration.
- Subqueries and Common Table Expressions.
- Window functions such as `ROW_NUMBER()`, `RANK()`, and `LAG()`.
- Daily and monthly performance analysis.
- Power-to-flow comparisons.
- High-load and high-power observations.
- Hour-to-hour power changes.

The SQLite database is a generated local artifact and is excluded from version control.

## 9. Excel Analysis

The Excel workbook is stored at:

`EXCEL/Compressor_Analysis.xlsx`

The Excel workflow covers data preparation, data-quality checks, missing-value analysis, duplicate detection, KPI analysis, outlier investigation, and exploratory analysis.

## 10. Power BI Dashboard

A Power BI-ready dataset has been generated at:

`OUTPUT/POWER_BI/compressor_powerbi.csv`

The file contains 10,800 records and includes the original sensor fields along with derived date, hour, month, and power-to-flow fields.

The interactive Power BI dashboard is the next phase of the project.

### Planned Dashboard Components

- KPI cards for compressor performance.
- Compressor-level power comparison.
- Monthly operating trends.
- Airflow and power relationships.
- Load and operating-status analysis.
- Interactive filters and compressor-level comparisons.
- Business findings and recommendations.

## 11. Business Implications

The current analysis supports exploratory comparisons and helps identify questions for further investigation.

Potential next steps include:

1. Compare compressors operating under similar pressure, airflow, and load conditions.
2. Validate energy calculations against actual meter readings if authorised real-world data becomes available.
3. Investigate unusual sensor readings before classifying them as faults.
4. Use the Power BI dashboard to communicate trends and performance indicators.
5. Evaluate anomaly-detection methods after establishing reliable data-quality checks and analytical baselines.

No real-world energy savings or equipment-performance improvements are claimed.

## 12. Project Structure

```text
Industrial-Compressor-Energy-Analytics/
│
├── DATA/
│   ├── RAW/
│   └── CLEANED/
│
├── EXCEL/
│   └── Compressor_Analysis.xlsx
│
├── OUTPUT/
│   ├── EDA/
│   │   └── charts/
│   └── POWER_BI/
│       └── compressor_powerbi.csv
│
├── PYTHON/
│   ├── 01_python_setup.py
│   ├── 02_python_fundamentals.py
│   ├── 03_pandas_basics.py
│   ├── 04_data_quality_and_cleaning.py
│   ├── 05_missing_values_and_imputation.py
│   ├── 06_outlier_analysis.py
│   ├── 07_exploratory_data_analysis.py
│   └── 08_sync_sql_database.py
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
```

This structure highlights the primary project folders. Additional files may be present in the repository.

## 13. How to Run the Python Analysis

Run the following commands from the project root in an environment where Python and the required packages are installed.

Install the main dependencies:

```bash
python -m pip install pandas matplotlib
```

Run the analysis scripts:

```bash
python PYTHON/04_data_quality_and_cleaning.py
python PYTHON/05_missing_values_and_imputation.py
python PYTHON/06_outlier_analysis.py
python PYTHON/07_exploratory_data_analysis.py
```

Run scripts in workflow order when setting up the project from scratch. Some steps may rely on files generated by earlier scripts.

### Synchronise the SQL Database

To rebuild the local SQLite data from the cleaned CSV:

```bash
python PYTHON/08_sync_sql_database.py
```

**Caution:** This script replaces the `compressor_data` table in the local database. Back up the database first if you need to preserve its current contents.

## 14. Project Status

### Completed

- [x] Synthetic dataset and data dictionary
- [x] Excel data cleaning and KPI analysis
- [x] SQL data cleaning and business analysis
- [x] SQL joins and time-series analysis
- [x] SQL window-function analysis
- [x] Python data-quality analysis
- [x] Missing-value investigation
- [x] Statistical outlier analysis
- [x] Python EDA and visualisations
- [x] Power BI-ready CSV preparation
- [x] SQL database synchronisation

### Upcoming

- [ ] Build the interactive Power BI dashboard
- [ ] Finalise the business-facing portfolio report
- [ ] Review and refine recommendations
- [ ] Explore a carefully validated anomaly-detection extension

## 15. Limitations

- The dataset is synthetic and may not reproduce real compressor behaviour.
- Correlations are descriptive and do not prove causation.
- Absolute power consumption does not establish equipment efficiency.
- Estimated energy depends on the hourly-reading assumption.
- Statistical outliers require investigation and are not automatically equipment faults.
- No verified energy savings, predictive accuracy, or maintenance outcomes are claimed.

## Author

**Ayush Kumar**
Computer Science Engineering
BITS Pilani

---

**Project focus:** Transforming synthetic sensor data into structured analysis, performance comparisons, and business-oriented insights using Python, SQL, and Excel.