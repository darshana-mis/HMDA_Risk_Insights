import duckdb
import os

# --- CONFIG ---
CSV_PATH = "D:/Darshana/Projects/Fifth_third/HMDA_Risk_Insights/data/raw/loan_applications.csv"         # path to your local CSV file
PARQUET_PATH = "D:/Darshana/Projects/Fifth_third/HMDA_Risk_Insights/data/processed/loan_applications.parquet"  # output Parquet file path

# Create directory if it doesn't exist
os.makedirs(os.path.dirname(PARQUET_PATH), exist_ok=True)

# Connect to DuckDB in-memory
con = duckdb.connect()

# Optional settings for faster conversion
con.execute("SET threads TO 4")
con.execute("SET memory_limit='2GB'")

# Convert CSV to Parquet
con.execute(f"""
    COPY (
        SELECT * FROM read_csv_auto('{CSV_PATH}', 
                                     IGNORE_ERRORS=TRUE, 
                                     DATEFORMAT='%Y-%m-%d',
                                     TIMESTAMPFORMAT='%Y-%m-%d %H:%M:%S')
    )
    TO '{PARQUET_PATH}'
    (FORMAT 'parquet', COMPRESSION 'zstd');
""")

print(f"✅ Successfully converted CSV to Parquet: {PARQUET_PATH}")
