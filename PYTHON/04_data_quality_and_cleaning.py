import os
import pandas as pd

# ============================================================
# DATA QUALITY ASSESSMENT AND CLEANING
# Dataset: Synthetic industrial compressor data
# ============================================================

INPUT_PATH = "DATA/RAW/synthetic_compressor_data_raw.csv"
OUTPUT_PATH = "DATA/CLEANED/compressor_data_cleaned.csv"

SENSOR_COLUMNS = [
    "Current_A",
    "Power_kW",
    "Pressure_bar",
    "Flow_m3h",
    "Temperature_C"
]

MISSING_SENSOR_COLUMNS = [
    "Pressure_bar",
    "Flow_m3h",
    "Temperature_C"
]


# ============================================================
# 1. LOAD RAW DATA
# ============================================================

df_raw = pd.read_csv(INPUT_PATH)

print("=" * 65)
print("DATA QUALITY ASSESSMENT AND CLEANING")
print("=" * 65)

print("\nOriginal dataset shape:", df_raw.shape)


# ============================================================
# 2. INITIAL DATA QUALITY ASSESSMENT
# ============================================================

print("\n" + "=" * 65)
print("INITIAL DATA QUALITY ASSESSMENT")
print("=" * 65)

print("\n--- Column Names ---")
print(df_raw.columns.tolist())

print("\n--- Data Types Before Conversion ---")
print(df_raw.dtypes)

print("\n--- Missing Values by Column ---")
print(df_raw.isna().sum().to_string())

print("\nTotal missing cells:", df_raw.isna().sum().sum())

print("\n--- Exact Duplicate Rows ---")
duplicate_count = df_raw.duplicated().sum()
print("Duplicate rows found:", duplicate_count)

print("\n--- Numeric Summary ---")
print(df_raw.describe().to_string())


# ============================================================
# 3. CHECK INVALID SENSOR VALUES
# ============================================================

print("\n" + "=" * 65)
print("INVALID SENSOR VALUE CHECKS")
print("=" * 65)

for column in SENSOR_COLUMNS:
    negative_count = (df_raw[column] < 0).sum()
    print(f"{column}: {negative_count} negative readings")

invalid_load = (
    (df_raw["Load_Percent"] < 0)
    | (df_raw["Load_Percent"] > 100)
).sum()

print("Load percentages outside 0-100:", invalid_load)

# These checks flag potential issues; they do not modify values.
# Physical plausibility must be assessed using appropriate
# equipment specifications and operating context.


# ============================================================
# 4. INSPECT MISSING-VALUE PATTERNS
# ============================================================

print("\n" + "=" * 65)
print("MISSING-VALUE PATTERNS")
print("=" * 65)

missing_rows = df_raw[df_raw.isna().any(axis=1)]

print("\nRows containing at least one missing value:",
      len(missing_rows))

print("\nFirst 10 rows with missing values:")
print(missing_rows.head(10).to_string(index=False))

print("\nMissing-value combinations for sensor columns:")
print(
    df_raw[MISSING_SENSOR_COLUMNS]
    .isna()
    .value_counts()
    .to_string()
)


# ============================================================
# 5. INSPECT DUPLICATE RECORDS
# ============================================================

print("\n" + "=" * 65)
print("DUPLICATE RECORD INSPECTION")
print("=" * 65)

duplicates = df_raw[df_raw.duplicated(keep=False)]

print("\nFirst 10 rows involved in duplicate groups:")
print(duplicates.head(10).to_string(index=False))

print("\nTotal rows involved in duplicate groups:", len(duplicates))


# ============================================================
# 6. INSPECT HIGHEST TEMPERATURE READINGS
# ============================================================

print("\n" + "=" * 65)
print("HIGHEST TEMPERATURE READINGS")
print("=" * 65)

print(
    df_raw.nlargest(10, "Temperature_C")[
        ["Timestamp", "Compressor_ID", "Temperature_C", "Power_kW"]
    ].to_string(index=False)
)


# ============================================================
# 7. CONVERT TIMESTAMPS AND CHECK PARSING FAILURES
# ============================================================

print("\n" + "=" * 65)
print("TIMESTAMP VALIDATION")
print("=" * 65)

df = df_raw.copy()

df["Timestamp"] = pd.to_datetime(
    df["Timestamp"],
    errors="coerce"
)

invalid_timestamp_count = df["Timestamp"].isna().sum()

print("Invalid timestamps after conversion:", invalid_timestamp_count)
print("Timestamp data type:", df["Timestamp"].dtype)

if invalid_timestamp_count > 0:
    print("\nRows with invalid timestamps:")
    print(
        df.loc[df["Timestamp"].isna()]
        .head(10)
        .to_string(index=False)
    )


# ============================================================
# 8. REMOVE EXACT DUPLICATES
# ============================================================

print("\n" + "=" * 65)
print("DUPLICATE REMOVAL")
print("=" * 65)

rows_before = len(df)

df_clean = df.drop_duplicates().copy()

rows_after = len(df_clean)
duplicates_removed = rows_before - rows_after

print("Rows before cleaning:", rows_before)
print("Exact duplicate rows removed:", duplicates_removed)
print("Rows after duplicate removal:", rows_after)


# ============================================================
# 9. PRESERVE MISSING VALUES
# ============================================================

print("\n" + "=" * 65)
print("MISSING VALUES AFTER DUPLICATE REMOVAL")
print("=" * 65)

print(df_clean.isna().sum().to_string())

print(
    "\nMissing sensor values are retained for further analysis. "
    "No imputation is performed in this script."
)


# ============================================================
# 10. SAVE CLEANED DATASET
# ============================================================

os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

df_clean.to_csv(OUTPUT_PATH, index=False)

print("\nCleaned dataset saved to:", OUTPUT_PATH)


# ============================================================
# 11. VALIDATE SAVED DATASET
# ============================================================

print("\n" + "=" * 65)
print("POST-CLEANING VALIDATION")
print("=" * 65)

saved_df = pd.read_csv(OUTPUT_PATH)

print("Saved dataset shape:", saved_df.shape)
print("Remaining exact duplicate rows:", saved_df.duplicated().sum())
print("Invalid timestamps in saved data:",
      pd.to_datetime(saved_df["Timestamp"], errors="coerce").isna().sum())

print("\nMissing values in saved dataset:")
print(saved_df.isna().sum().to_string())

print("\nRows removed:", len(df_raw) - len(saved_df))
print("Original raw dataset was not modified.")

print("\n" + "=" * 65)
print("DATA QUALITY AND CLEANING COMPLETED")
print("=" * 65)
