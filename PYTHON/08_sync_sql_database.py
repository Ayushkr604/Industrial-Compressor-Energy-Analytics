import sqlite3
import pandas as pd
from pathlib import Path

csv_path = Path("DATA/CLEANED/compressor_data_cleaned.csv")
db_path = Path("SQL/compressor_analysis.db")

df = pd.read_csv(csv_path)

with sqlite3.connect(db_path) as conn:
    df.to_sql("compressor_data_new", conn, if_exists="replace", index=False)

    conn.execute("DROP VIEW IF EXISTS cleaned_compressor_data")
    conn.execute("DROP TABLE IF EXISTS compressor_data")

    conn.execute(
        "ALTER TABLE compressor_data_new RENAME TO compressor_data"
    )

    conn.execute("""
        CREATE VIEW cleaned_compressor_data AS
        SELECT DISTINCT *
        FROM compressor_data
        WHERE (Power_kW >= 0 OR Power_kW IS NULL)
          AND (Current_A >= 0 OR Current_A IS NULL)
          AND (Pressure_bar >= 0 OR Pressure_bar IS NULL)
          AND (Flow_m3h >= 0 OR Flow_m3h IS NULL)
          AND (Temperature_C >= 0 OR Temperature_C IS NULL)
          AND (Load_Percent BETWEEN 0 AND 100 OR Load_Percent IS NULL)
    """)

    result = conn.execute("""
        SELECT
            COUNT(*),
            SUM(Pressure_bar IS NULL),
            SUM(Flow_m3h IS NULL),
            SUM(Temperature_C IS NULL)
        FROM cleaned_compressor_data
    """).fetchone()

print("SQL database synchronized.")
print("Rows, missing pressure, missing flow, missing temperature:", result)
