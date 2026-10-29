import pandas as pd

# ============================================================
# MISSING VALUES AND SAFE IMPUTATION
# ============================================================

INPUT_PATH = "DATA/CLEANED/compressor_data_cleaned.csv"
OUTPUT_PATH = "DATA/CLEANED/compressor_data_safe_interpolation.csv"

SENSOR_COLUMNS = [
    "Pressure_bar",
    "Flow_m3h",
    "Temperature_C"
]

KEY_COLUMNS = ["Timestamp", "Compressor_ID"]


# ============================================================
# 1. LOAD AND PREPARE DATA
# ============================================================

df = pd.read_csv(INPUT_PATH)

df["Timestamp"] = pd.to_datetime(df["Timestamp"])

df = df.sort_values(
    ["Compressor_ID", "Timestamp"]
).reset_index(drop=True)

print("=" * 65)
print("MISSING VALUES AND SAFE IMPUTATION")
print("=" * 65)

print("\nDataset shape:", df.shape)
print("Unique compressors:", df["Compressor_ID"].nunique())


# ============================================================
# 2. MISSING-VALUE COUNTS AND PERCENTAGES
# ============================================================

print("\n" + "=" * 65)
print("MISSING VALUES BY COLUMN")
print("=" * 65)

missing_counts = df.isna().sum()
missing_percentages = (missing_counts / len(df)) * 100

missing_summary = pd.DataFrame({
    "Missing_Count": missing_counts,
    "Missing_Percentage": missing_percentages.round(2)
})

print(missing_summary.to_string())

missing_rows = df[df[SENSOR_COLUMNS].isna().any(axis=1)]

print("\nRows containing at least one missing sensor reading:",
      len(missing_rows))

print("Total missing sensor cells:",
      df[SENSOR_COLUMNS].isna().sum().sum())

print("\nFirst 10 rows containing missing sensor readings:")

print(
    missing_rows.head(10).to_string(index=False)
)


# ============================================================
# 3. MISSING VALUES BY COMPRESSOR
# ============================================================

print("\n" + "=" * 65)
print("MISSING VALUES BY COMPRESSOR")
print("=" * 65)

missing_by_compressor = (
    df.groupby("Compressor_ID")[SENSOR_COLUMNS]
    .apply(lambda group: group.isna().sum())
)

print(missing_by_compressor.to_string())


# ============================================================
# 4. MISSING VALUES BY COMPRESSOR AND OPERATING STATUS
# ============================================================

print("\n" + "=" * 65)
print("MISSING VALUES BY COMPRESSOR AND STATUS")
print("=" * 65)

for column in SENSOR_COLUMNS:
    print(f"\n{column}:")

    missing_by_status = (
        df.loc[df[column].isna()]
        .groupby(["Compressor_ID", "Running_Status"])
        .size()
    )

    if missing_by_status.empty:
        print("No missing values.")
    else:
        print(missing_by_status.to_string())


# ============================================================
# 5. INSPECT NEIGHBORING OBSERVATIONS
# ============================================================

print("\n" + "=" * 65)
print("EXAMPLES OF MISSING READINGS AND NEIGHBORS")
print("=" * 65)

for _, missing_row in missing_rows.head(5).iterrows():

    compressor_id = missing_row["Compressor_ID"]
    timestamp = missing_row["Timestamp"]

    compressor_data = (
        df[df["Compressor_ID"] == compressor_id]
        .sort_values("Timestamp")
        .reset_index(drop=True)
    )

    matching_positions = compressor_data.index[
        compressor_data["Timestamp"] == timestamp
    ]

    if len(matching_positions) == 0:
        continue

    position = matching_positions[0]

    start = max(0, position - 1)
    end = min(len(compressor_data), position + 2)

    print("\n" + "-" * 65)
    print("Compressor:", compressor_id)
    print("Missing timestamp:", timestamp)

    print(
        compressor_data.iloc[start:end][
            ["Timestamp", "Running_Status"] + SENSOR_COLUMNS
        ].to_string(index=False)
    )


# ============================================================
# 6. CREATE A SEPARATE DATASET FOR SAFE IMPUTATION
# ============================================================

print("\n" + "=" * 65)
print("SAFE INTERPOLATION")
print("=" * 65)

# Preserve the cleaned source and its observed measurements.
df_safe = df.copy()

# Record which sensor values were originally missing.
# These flags remain True even after a value is estimated.
for column in SENSOR_COLUMNS:
    df_safe[f"{column}_Was_Missing"] = df[column].isna()


# ============================================================
# 7. INTERPOLATE WITHIN CONTINUOUS RUNNING PERIODS ONLY
# ============================================================

for compressor_id in df["Compressor_ID"].unique():

    compressor_mask = df["Compressor_ID"] == compressor_id

    compressor_data = df.loc[compressor_mask].copy()

    # Every stopped record breaks the running period.
    compressor_data["Running_Group"] = (
        compressor_data["Running_Status"]
        .ne("Running")
        .cumsum()
    )

    for group_id in compressor_data["Running_Group"].unique():

        group_mask = (
            compressor_data["Running_Group"].eq(group_id)
            & compressor_data["Running_Status"].eq("Running")
        )

        group_indices = compressor_data.index[group_mask]

        if len(group_indices) == 0:
            continue

        for column in SENSOR_COLUMNS:

            original_values = df.loc[group_indices, column]

            interpolated_values = original_values.interpolate(
                method="linear",
                limit_area="inside"
            )

            df_safe.loc[group_indices, column] = interpolated_values


# ============================================================
# 8. REPORT IMPUTATION RESULTS
# ============================================================

print("\nMissing values before interpolation:")

print(df[SENSOR_COLUMNS].isna().sum().to_string())

print("\nMissing values after safe interpolation:")

print(df_safe[SENSOR_COLUMNS].isna().sum().to_string())

print("\nImputation summary:")

imputation_summary = []

for column in SENSOR_COLUMNS:

    estimated = (
        df[column].isna()
        & df_safe[column].notna()
    ).sum()

    still_missing = df_safe[column].isna().sum()

    originally_missing = df[column].isna().sum()

    imputation_summary.append({
        "Sensor": column,
        "Originally_Missing": int(originally_missing),
        "Estimated": int(estimated),
        "Still_Missing": int(still_missing)
    })

imputation_summary = pd.DataFrame(imputation_summary)

print(imputation_summary.to_string(index=False))


# ============================================================
# 9. VALIDATE ROW MATCHING AND PRESERVATION OF MEASUREMENTS
# ============================================================

print("\n" + "=" * 65)
print("VALIDATION")
print("=" * 65)

# Match by timestamp and compressor, not by row position alone.
comparison = df.merge(
    df_safe,
    on=KEY_COLUMNS,
    how="outer",
    suffixes=("_original", "_result"),
    indicator=True,
    validate="one_to_one"
)

matched_rows = (comparison["_merge"] == "both").sum()
unmatched_rows = (comparison["_merge"] != "both").sum()

print("\nOriginal row count:", len(df))
print("Result row count:", len(df_safe))
print("Matched rows:", matched_rows)
print("Unmatched rows:", unmatched_rows)

print("\nOriginally observed values changed:")

for column in SENSOR_COLUMNS:

    original_col = f"{column}_original"
    result_col = f"{column}_result"

    originally_present = comparison[original_col].notna()

    changed = originally_present & (
        comparison[result_col].isna()
        | (
            comparison[original_col]
            .sub(comparison[result_col])
            .abs()
            .gt(1e-9)
        )
    )

    print(f"{column}: {int(changed.sum())}")


# Check whether stopped rows were imputed.
print("\nEstimated values in originally stopped rows:")

original_stopped = df["Running_Status"].eq("Stopped").to_numpy()

for column in SENSOR_COLUMNS:

    estimated = (
        df[column].isna()
        & df_safe[column].notna()
    ).to_numpy()

    stopped_estimates = (original_stopped & estimated).sum()

    print(f"{column}: {int(stopped_estimates)}")


# ============================================================
# 10. SAVE RESULTS SEPARATELY
# ============================================================

df_safe.to_csv(OUTPUT_PATH, index=False)

print("\n" + "=" * 65)
print("COMPLETED")
print("=" * 65)

print("Output saved to:", OUTPUT_PATH)
print("Original cleaned dataset was not modified.")
print("Originally missing values are marked with *_Was_Missing flags.")
print("Interpolated values are estimates, not original measurements.")
