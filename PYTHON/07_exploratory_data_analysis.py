import os
import pandas as pd
import matplotlib.pyplot as plt

# ============================================================
# INDUSTRIAL COMPRESSOR ENERGY ANALYTICS
# EXPLORATORY DATA ANALYSIS (EDA)
# Dataset: Synthetic industrial compressor data
# ============================================================

INPUT_PATH = "DATA/CLEANED/compressor_data_cleaned.csv"
OUTPUT_DIR = "OUTPUT/EDA"
CHART_DIR = os.path.join(OUTPUT_DIR, "charts")

os.makedirs(CHART_DIR, exist_ok=True)

# ============================================================
# 1. LOAD DATA
# ============================================================

df = pd.read_csv(INPUT_PATH)

df["Timestamp"] = pd.to_datetime(
    df["Timestamp"],
    errors="coerce"
)

df = df.sort_values(
    ["Compressor_ID", "Timestamp"]
).reset_index(drop=True)

print("=" * 70)
print("INDUSTRIAL COMPRESSOR ENERGY ANALYTICS — EDA")
print("=" * 70)

print("\nDataset shape:", df.shape)
print("Number of compressors:", df["Compressor_ID"].nunique())
print("Date range:", df["Timestamp"].min(), "to", df["Timestamp"].max())
print("Duplicate rows:", df.duplicated().sum())

# ============================================================
# 2. DATASET OVERVIEW
# ============================================================

print("\n" + "=" * 70)
print("DATASET OVERVIEW")
print("=" * 70)

print("\nColumn data types:")
print(df.dtypes.to_string())

print("\nMissing values:")
print(df.isna().sum().to_string())

print("\nRunning status counts:")
print(df["Running_Status"].value_counts(dropna=False).to_string())

print("\nObservations per compressor:")
print(df["Compressor_ID"].value_counts().sort_index().to_string())

# ============================================================
# 3. COMPRESSOR-LEVEL SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("COMPRESSOR-LEVEL SUMMARY")
print("=" * 70)

summary = (
    df.groupby("Compressor_ID")
    .agg(
        Total_Readings=("Timestamp", "count"),
        Running_Readings=(
            "Running_Status",
            lambda s: (s == "Running").sum()
        ),
        Stopped_Readings=(
            "Running_Status",
            lambda s: (s == "Stopped").sum()
        ),
        Average_Current_A=("Current_A", "mean"),
        Average_Power_kW=("Power_kW", "mean"),
        Average_Pressure_bar=("Pressure_bar", "mean"),
        Average_Flow_m3h=("Flow_m3h", "mean"),
        Average_Temperature_C=("Temperature_C", "mean"),
        Average_Load_Percent=("Load_Percent", "mean"),
    )
    .round(2)
)

print(summary.to_string())

summary.to_csv(
    os.path.join(OUTPUT_DIR, "compressor_summary.csv")
)

# ============================================================
# 4. OPERATING STATUS ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("OPERATING STATUS ANALYSIS")
print("=" * 70)

status_summary = (
    df.groupby(["Compressor_ID", "Running_Status"])
    .size()
    .unstack(fill_value=0)
)

status_summary["Total_Readings"] = status_summary.sum(axis=1)

status_summary["Running_Percent"] = (
    status_summary.get("Running", 0)
    / status_summary["Total_Readings"]
    * 100
).round(2)

status_summary["Stopped_Percent"] = (
    status_summary.get("Stopped", 0)
    / status_summary["Total_Readings"]
    * 100
).round(2)

print(status_summary.to_string())

status_summary.to_csv(
    os.path.join(OUTPUT_DIR, "operating_status_summary.csv")
)

# ============================================================
# 5. VALIDATE TIMESTAMP INTERVALS
# ============================================================

print("\n" + "=" * 70)
print("TIMESTAMP INTERVAL VALIDATION")
print("=" * 70)

df["Time_Gap_Hours"] = (
    df.groupby("Compressor_ID")["Timestamp"]
    .diff()
    .dt.total_seconds()
    / 3600
)

print("\nTime gap distribution in hours:")
print(df["Time_Gap_Hours"].describe().round(2).to_string())

print("\nTime gaps that are not one hour:")
print(
    df.loc[
        df["Time_Gap_Hours"].notna()
        & (df["Time_Gap_Hours"] != 1),
        ["Timestamp", "Compressor_ID", "Time_Gap_Hours"]
    ]
    .head(20)
    .to_string(index=False)
)

print("\nEDA section 1 completed.")
print("Results saved in:", OUTPUT_DIR)


# ============================================================
# 6. RUNNING-ONLY POWER ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("RUNNING-ONLY POWER ANALYSIS")
print("=" * 70)

running_df = df[df["Running_Status"] == "Running"].copy()

running_power_summary = (
    running_df.groupby("Compressor_ID")
    .agg(
        Running_Readings=("Power_kW", "count"),
        Average_Power_kW=("Power_kW", "mean"),
        Median_Power_kW=("Power_kW", "median"),
        Min_Power_kW=("Power_kW", "min"),
        Max_Power_kW=("Power_kW", "max"),
        Average_Current_A=("Current_A", "mean"),
        Average_Flow_m3h=("Flow_m3h", "mean"),
        Average_Load_Percent=("Load_Percent", "mean"),
    )
    .round(2)
    .sort_values("Average_Power_kW", ascending=False)
)

print("\nRunning-only compressor ranking:")
print(running_power_summary.to_string())

running_power_summary.to_csv(
    os.path.join(OUTPUT_DIR, "running_power_summary.csv")
)


# ============================================================
# 7. ESTIMATE ENERGY CONSUMPTION
# ============================================================

print("\n" + "=" * 70)
print("ESTIMATED ENERGY CONSUMPTION")
print("=" * 70)

# Each row represents an hourly observation.
# This estimate assumes Power_kW represents average power
# throughout the following one-hour interval.
#
# Verify this assumption before treating the result as
# a measured energy figure.

df["Estimated_Energy_kWh"] = df["Power_kW"] * 1.0

energy_summary = (
    df.groupby("Compressor_ID")
    .agg(
        Total_Observations=("Timestamp", "count"),
        Estimated_Energy_kWh=("Estimated_Energy_kWh", "sum"),
        Average_Power_kW=("Power_kW", "mean"),
    )
    .round(2)
    .sort_values("Estimated_Energy_kWh", ascending=False)
)

print("\nEstimated energy ranking:")
print(energy_summary.to_string())

print(
    "\nCaution: these are estimates derived from synthetic hourly data, "
    "not independently measured energy consumption."
)

energy_summary.to_csv(
    os.path.join(OUTPUT_DIR, "estimated_energy_summary.csv")
)


# ============================================================
# 8. MONTHLY POWER TRENDS
# ============================================================

print("\n" + "=" * 70)
print("MONTHLY POWER TRENDS")
print("=" * 70)

df["Month"] = df["Timestamp"].dt.to_period("M").astype(str)

monthly_power = (
    running_df.assign(
        Month=running_df["Timestamp"].dt.to_period("M").astype(str)
    )
    .groupby(["Month", "Compressor_ID"])["Power_kW"]
    .mean()
    .unstack()
    .round(2)
)

print("\nAverage running power by month (kW):")
print(monthly_power.to_string())

monthly_power.to_csv(
    os.path.join(OUTPUT_DIR, "monthly_running_power.csv")
)

ax = monthly_power.plot(
    kind="line",
    marker="o",
    figsize=(10, 6)
)

ax.set_title("Monthly Average Running Power by Compressor")
ax.set_xlabel("Month")
ax.set_ylabel("Average Power (kW)")
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(
    os.path.join(CHART_DIR, "monthly_running_power.png"),
    dpi=150
)
plt.close()


# ============================================================
# 9. COMPRESSOR POWER COMPARISON
# ============================================================

ax = running_power_summary["Average_Power_kW"].sort_values().plot(
    kind="bar",
    figsize=(9, 5)
)

ax.set_title("Average Running Power by Compressor")
ax.set_xlabel("Compressor")
ax.set_ylabel("Average Power (kW)")
ax.grid(axis="y", alpha=0.3)

plt.tight_layout()
plt.savefig(
    os.path.join(CHART_DIR, "running_power_comparison.png"),
    dpi=150
)
plt.close()


# ============================================================
# 10. SENSOR CORRELATIONS
# ============================================================

print("\n" + "=" * 70)
print("SENSOR CORRELATION ANALYSIS")
print("=" * 70)

sensor_columns = [
    "Current_A",
    "Power_kW",
    "Pressure_bar",
    "Flow_m3h",
    "Temperature_C",
    "Load_Percent",
]

correlation_matrix = running_df[sensor_columns].corr()

print("\nRunning-only sensor correlation matrix:")
print(correlation_matrix.round(3).to_string())

correlation_matrix.to_csv(
    os.path.join(OUTPUT_DIR, "sensor_correlation_matrix.csv")
)

fig, ax = plt.subplots(figsize=(9, 7))

image = ax.imshow(
    correlation_matrix,
    vmin=-1,
    vmax=1,
    aspect="auto"
)

ax.set_xticks(range(len(sensor_columns)))
ax.set_yticks(range(len(sensor_columns)))
ax.set_xticklabels(sensor_columns, rotation=45, ha="right")
ax.set_yticklabels(sensor_columns)

for i in range(len(sensor_columns)):
    for j in range(len(sensor_columns)):
        ax.text(
            j,
            i,
            f"{correlation_matrix.iloc[i, j]:.2f}",
            ha="center",
            va="center"
        )

fig.colorbar(image, ax=ax, label="Correlation")
ax.set_title("Running-Only Sensor Correlations")

plt.tight_layout()
plt.savefig(
    os.path.join(CHART_DIR, "sensor_correlation_matrix.png"),
    dpi=150
)
plt.close()


# ============================================================
# 11. SPECIFIC POWER ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("SPECIFIC POWER ANALYSIS")
print("=" * 70)

# Use only running compressors with valid, positive airflow.
specific_power_df = df[
    (df["Running_Status"] == "Running") &
    (df["Flow_m3h"].notna()) &
    (df["Flow_m3h"] > 0) &
    (df["Power_kW"].notna()) &
    (df["Power_kW"] >= 0)
].copy()

# Preliminary power-to-airflow ratio.
# This is a proxy, not an officially validated efficiency metric.
specific_power_df["Power_per_Flow"] = (
    specific_power_df["Power_kW"] /
    specific_power_df["Flow_m3h"]
)

specific_power_summary = (
    specific_power_df
    .groupby("Compressor_ID")
    .agg(
        Readings=("Power_per_Flow", "count"),
        Average_Power_kW=("Power_kW", "mean"),
        Average_Flow_m3h=("Flow_m3h", "mean"),
        Average_Power_per_Flow=("Power_per_Flow", "mean"),
        Median_Power_per_Flow=("Power_per_Flow", "median")
    )
    .reset_index()
    .sort_values("Average_Power_per_Flow")
)

specific_power_summary.to_csv(
    os.path.join(OUTPUT_DIR, "specific_power_summary.csv"),
    index=False
)

print("\nPreliminary power-to-flow comparison:")
print(specific_power_summary.round(4).to_string(index=False))

print(
    "\nInterpretation note: Lower power-to-flow ratios may indicate "
    "better power use relative to airflow, but comparisons require "
    "comparable operating conditions and validated measurements."
)


# ============================================================
# 12. TEMPERATURE INVESTIGATION
# ============================================================

print("\n" + "=" * 70)
print("TEMPERATURE INVESTIGATION")
print("=" * 70)

# Analyze running compressors with valid temperature readings.
temperature_df = df[
    (df["Running_Status"] == "Running") &
    (df["Temperature_C"].notna())
].copy()

# 1. Temperature summary by compressor.
temperature_summary = (
    temperature_df
    .groupby("Compressor_ID")
    .agg(
        Readings=("Temperature_C", "count"),
        Average_Temperature_C=("Temperature_C", "mean"),
        Median_Temperature_C=("Temperature_C", "median"),
        Minimum_Temperature_C=("Temperature_C", "min"),
        Maximum_Temperature_C=("Temperature_C", "max"),
        Average_Power_kW=("Power_kW", "mean"),
        Average_Current_A=("Current_A", "mean"),
        Average_Load_Percent=("Load_Percent", "mean")
    )
    .reset_index()
    .sort_values("Average_Temperature_C", ascending=False)
)

temperature_summary.to_csv(
    os.path.join(OUTPUT_DIR, "temperature_summary.csv"),
    index=False
)

print("\nTemperature summary by compressor:")
print(temperature_summary.round(2).to_string(index=False))

# 2. Identify unusually high temperatures using the IQR method.
q1 = temperature_df["Temperature_C"].quantile(0.25)
q3 = temperature_df["Temperature_C"].quantile(0.75)
iqr = q3 - q1
upper_bound = q3 + 1.5 * iqr

high_temperature_df = temperature_df[
    temperature_df["Temperature_C"] > upper_bound
].copy()

high_temperature_df = high_temperature_df.sort_values(
    "Temperature_C",
    ascending=False
)

high_temperature_df.to_csv(
    os.path.join(OUTPUT_DIR, "high_temperature_readings.csv"),
    index=False
)

print(f"\nTemperature IQR upper bound: {upper_bound:.2f} °C")
print(f"Readings above the IQR upper bound: {len(high_temperature_df)}")

if not high_temperature_df.empty:
    print("\nHighest-temperature readings:")
    print(
        high_temperature_df[
            [
                "Timestamp",
                "Compressor_ID",
                "Temperature_C",
                "Power_kW",
                "Current_A",
                "Load_Percent"
            ]
            ].head(10).to_string(index=False)
    )

# 3. Examine correlations between temperature and operating variables.
temperature_correlations = temperature_df[
    [
        "Temperature_C",
        "Power_kW",
        "Current_A",
        "Load_Percent",
        "Flow_m3h",
        "Pressure_bar"
    ]
].corr()

temperature_correlations.to_csv(
    os.path.join(OUTPUT_DIR, "temperature_correlations.csv")
)

print("\nTemperature correlations with operating variables:")
print(
    temperature_correlations["Temperature_C"]
    .drop("Temperature_C")
    .sort_values(ascending=False)
    .round(3)
    .to_string()
)

# 4. Plot average running temperature by compressor.
plt.figure(figsize=(10, 6))

temperature_plot = (
    temperature_df
    .groupby("Compressor_ID")["Temperature_C"]
    .mean()
    .sort_values(ascending=False)
)

temperature_plot.plot(kind="bar")

plt.title("Average Running Temperature by Compressor")
plt.xlabel("Compressor")
plt.ylabel("Average Temperature (°C)")
plt.xticks(rotation=0)
plt.tight_layout()

plt.savefig(
    os.path.join(CHART_DIR, "average_running_temperature.png"),
    dpi=300
)

plt.close()

print("\nTemperature investigation completed.")

# ============================================================
# 14. FINAL OUTPUT SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("EDA ANALYSIS COMPLETED")
print("=" * 70)

print("\nTables saved in:", OUTPUT_DIR)
print("Charts saved in:", CHART_DIR)

print("\nGenerated tables:")
for filename in sorted(os.listdir(OUTPUT_DIR)):
    if filename.endswith(".csv"):
        print("-", filename)

print("\nGenerated charts:")
for filename in sorted(os.listdir(CHART_DIR)):
    if filename.endswith(".png"):
        print("-", filename)


# ============================================================
# 13. COMPRESSOR OPERATING PATTERN ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("COMPRESSOR OPERATING PATTERN ANALYSIS")
print("=" * 70)

# Sort observations chronologically for each compressor.
operating_df = df.sort_values(
    ["Compressor_ID", "Timestamp"]
).copy()

# Identify changes in operating status.
operating_df["Previous_Status"] = (
    operating_df.groupby("Compressor_ID")["Running_Status"].shift(1)
)

operating_df["Status_Changed"] = (
    operating_df["Running_Status"]
    .ne(operating_df["Previous_Status"])
    .where(operating_df["Previous_Status"].notna(), False)
)

# Summarize running and stopped observations.
operating_summary = (
    operating_df.groupby("Compressor_ID")
    .agg(
        Total_Readings=("Running_Status", "size"),
        Running_Readings=(
            "Running_Status",
            lambda s: (s == "Running").sum()
        ),
        Stopped_Readings=(
            "Running_Status",
            lambda s: (s == "Stopped").sum()
        ),
        Status_Changes=("Status_Changed", "sum")
    )
)

operating_summary["Running_Percent"] = (
    operating_summary["Running_Readings"]
    / operating_summary["Total_Readings"] * 100
)

operating_summary["Stopped_Percent"] = (
    operating_summary["Stopped_Readings"]
    / operating_summary["Total_Readings"] * 100
)

operating_summary = operating_summary.round(2)

operating_summary.to_csv(
    os.path.join(OUTPUT_DIR, "operating_pattern_summary.csv")
)

print("\nOperating pattern summary:")
print(operating_summary.to_string())

# Identify continuous stopped periods.
operating_df["Stopped_Flag"] = (
    operating_df["Running_Status"] == "Stopped"
)

operating_df["Stopped_Group"] = (
    operating_df.groupby("Compressor_ID")["Stopped_Flag"]
    .transform(
        lambda s: s.ne(s.shift()).cumsum()
    )
)

stopped_df = operating_df[
    operating_df["Stopped_Flag"]
].copy()

if not stopped_df.empty:
    stopped_periods = (
        stopped_df.groupby(["Compressor_ID", "Stopped_Group"])
        .agg(
            Start_Time=("Timestamp", "min"),
            End_Time=("Timestamp", "max"),
            Stopped_Readings=("Timestamp", "size")
        )
        .reset_index()
    )

        # Calculate the observed span between the first and last
    # stopped timestamps, then estimate duration assuming each
    # hourly reading represents one full hour of stopped operation.
    stopped_periods["Observed_Span_Hours"] = (
        stopped_periods["End_Time"] - stopped_periods["Start_Time"]
    ).dt.total_seconds() / 3600

    stopped_periods["Estimated_Duration_Hours"] = (
        stopped_periods["Observed_Span_Hours"] + 1
    )
    
    stopped_periods.to_csv(
        os.path.join(OUTPUT_DIR, "stopped_periods.csv"),
        index=False
    )

    stopped_duration_summary = (
        stopped_periods.groupby("Compressor_ID")
        .agg(
            Number_of_Stopped_Periods=("Stopped_Group", "count"),
            Average_Stopped_Duration_Hours=(
                "Estimated_Duration_Hours", "mean"
            ),
            Maximum_Stopped_Duration_Hours=(
                "Estimated_Duration_Hours", "max"
            )
        )
        .round(2)
    )

    stopped_duration_summary.to_csv(
        os.path.join(OUTPUT_DIR, "stopped_duration_summary.csv")
    )

    print("\nStopped duration summary:")
    print(stopped_duration_summary.to_string())

    print(
        "\nCaution: durations are estimated from hourly status observations. "
        "Exact start and end times may differ from actual equipment events."
    )

print("\nOperating pattern analysis completed.")