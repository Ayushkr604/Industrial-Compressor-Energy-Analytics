# Industrial Compressor Energy Analytics
# Consolidated Outlier Analysis

import pandas as pd
import os

# --------------------------------------------------
# 1. LOAD DATA
# --------------------------------------------------

FILE_PATH = "DATA/CLEANED/compressor_data_cleaned.csv"
OUTPUT_DIR = "DATA/CLEANED"

os.makedirs(OUTPUT_DIR, exist_ok=True)

df = pd.read_csv(FILE_PATH)

sensor_columns = [
    "Current_A",
    "Power_kW",
    "Pressure_bar",
    "Flow_m3h",
    "Temperature_C",
    "Load_Percent"
]

required_columns = [
    "Timestamp",
    "Compressor_ID",
    "Running_Status",
    *sensor_columns
]

missing_columns = [
    column for column in required_columns
    if column not in df.columns
]

if missing_columns:
    raise ValueError(
        f"Required columns are missing: {missing_columns}"
    )

print("INDUSTRIAL COMPRESSOR OUTLIER ANALYSIS")
print("=" * 75)
print("Dataset shape:", df.shape)
print("Original data will not be modified.")


# --------------------------------------------------
# 2. REUSABLE IQR ANALYSIS FUNCTION
# --------------------------------------------------

def analyze_group(group, group_details):
    """Calculate IQR bounds and identify potential outliers."""

    results = []

    for column in sensor_columns:
        values = group[column].dropna()

        if len(values) < 4:
            continue

        q1 = values.quantile(0.25)
        q3 = values.quantile(0.75)
        iqr = q3 - q1

        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr

        mask = (
            group[column].notna()
            & (
                (group[column] < lower_bound)
                | (group[column] > upper_bound)
            )
        )

        flagged_rows = group.loc[mask]

        results.append({
            **group_details,
            "Sensor": column,
            "Readings": len(values),
            "Q1": round(q1, 2),
            "Q3": round(q3, 2),
            "IQR": round(iqr, 2),
            "Lower_Bound": round(lower_bound, 2),
            "Upper_Bound": round(upper_bound, 2),
            "Outlier_Count": int(mask.sum()),
            "Outlier_Percentage": round(
                mask.sum() / len(values) * 100, 2
            )
        })

    return results


# --------------------------------------------------
# 3. GLOBAL IQR ANALYSIS
# --------------------------------------------------

print("\n\nGLOBAL IQR ANALYSIS")
print("=" * 75)

global_results = analyze_group(
    df,
    {"Analysis_Level": "Global"}
)

global_df = pd.DataFrame(global_results)

print(
    global_df[
        [
            "Sensor",
            "Readings",
            "Lower_Bound",
            "Upper_Bound",
            "Outlier_Count",
            "Outlier_Percentage"
        ]
    ].to_string(index=False)
)

global_df.to_csv(
    os.path.join(OUTPUT_DIR, "outlier_analysis_global.csv"),
    index=False
)


# --------------------------------------------------
# 4. OUTLIERS BY COMPRESSOR
# --------------------------------------------------

print("\n\nOUTLIER ANALYSIS BY COMPRESSOR")
print("=" * 75)

compressor_results = []

for compressor_id, group in df.groupby("Compressor_ID"):
    compressor_results.extend(
        analyze_group(
            group,
            {
                "Analysis_Level": "Compressor",
                "Compressor_ID": compressor_id
            }
        )
    )

compressor_df = pd.DataFrame(compressor_results)

print(
    compressor_df[
        [
            "Compressor_ID",
            "Sensor",
            "Readings",
            "Outlier_Count",
            "Outlier_Percentage"
        ]
    ].to_string(index=False)
)

compressor_df.to_csv(
    os.path.join(OUTPUT_DIR, "outlier_analysis_by_compressor.csv"),
    index=False
)


# --------------------------------------------------
# 5. OUTLIERS BY COMPRESSOR AND OPERATING STATUS
# --------------------------------------------------

print("\n\nOUTLIER ANALYSIS BY COMPRESSOR AND STATUS")
print("=" * 75)

status_results = []

for (compressor_id, status), group in df.groupby(
    ["Compressor_ID", "Running_Status"]
):
    status_results.extend(
        analyze_group(
            group,
            {
                "Analysis_Level": "Compressor_Status",
                "Compressor_ID": compressor_id,
                "Running_Status": status
            }
        )
    )

status_df = pd.DataFrame(status_results)

print(
    status_df[
        [
            "Compressor_ID",
            "Running_Status",
            "Sensor",
            "Readings",
            "Outlier_Count",
            "Outlier_Percentage"
        ]
    ].to_string(index=False)
)

status_df.to_csv(
    os.path.join(OUTPUT_DIR, "outlier_analysis_by_status.csv"),
    index=False
)


# --------------------------------------------------
# 6. INVESTIGATE INDIVIDUAL FLAGGED READINGS
# --------------------------------------------------

print("\n\nDETAILED OUTLIER INVESTIGATION")
print("=" * 75)

investigation_records = []

for (compressor_id, status), group in df.groupby(
    ["Compressor_ID", "Running_Status"]
):
    for column in sensor_columns:
        values = group[column].dropna()

        if len(values) < 4:
            continue

        q1 = values.quantile(0.25)
        q3 = values.quantile(0.75)
        iqr = q3 - q1

        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr

        mask = (
            group[column].notna()
            & (
                (group[column] < lower_bound)
                | (group[column] > upper_bound)
            )
        )

        for _, row in group.loc[mask].iterrows():
            investigation_records.append({
                "Timestamp": row["Timestamp"],
                "Compressor_ID": compressor_id,
                "Running_Status": status,
                "Flagged_Sensor": column,
                "Flagged_Value": row[column],
                "Lower_Bound": round(lower_bound, 2),
                "Upper_Bound": round(upper_bound, 2),
                **{
                    sensor: row[sensor]
                    for sensor in sensor_columns
                }
            })

investigation_df = pd.DataFrame(investigation_records)

if not investigation_df.empty:
    investigation_df = investigation_df.sort_values(
        ["Timestamp", "Compressor_ID", "Flagged_Sensor"]
    )

investigation_path = os.path.join(
    OUTPUT_DIR,
    "outlier_investigation.csv"
)

investigation_df.to_csv(
    investigation_path,
    index=False
)

print("Total flagged sensor readings:", len(investigation_df))

if not investigation_df.empty:
    print("\nFlagged readings by sensor:")
    print(
        investigation_df["Flagged_Sensor"]
        .value_counts()
        .to_string()
    )

    print("\nFlagged readings by compressor:")
    print(
        investigation_df["Compressor_ID"]
        .value_counts()
        .to_string()
    )

    print("\nFlagged readings by operating status:")
    print(
        investigation_df["Running_Status"]
        .value_counts()
        .to_string()
    )

    print("\nFirst 10 flagged readings:")
    print(
        investigation_df.head(10).to_string(index=False)
    )


# --------------------------------------------------
# 7. COMPLETION SUMMARY
# --------------------------------------------------

print("\n\nANALYSIS COMPLETE")
print("=" * 75)

print("Output files:")
print("- outlier_analysis_global.csv")
print("- outlier_analysis_by_compressor.csv")
print("- outlier_analysis_by_status.csv")
print("- outlier_investigation.csv")

print("\nInterpretation notes:")
print("- IQR flags indicate potential statistical outliers.")
print("- They do not automatically indicate equipment faults.")
print("- No original sensor readings were changed.")
print("- No records were deleted.")