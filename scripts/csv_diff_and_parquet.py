import os
import duckdb
from datetime import datetime

# ========= CONFIG (edit these) =========
CSV_PATH       = r"D:/Darshana/Projects/Fifth_third/HMDA_Risk_Insights/data/loan_applications.csv"
PARQUET_PATH   = r"D:/Darshana/Projects/Fifth_third/HMDA_Risk_Insights/data/loan_applications.parquet"
BAD_ROWS_PATH  = r"D:/Darshana/Projects/Fifth_third/data/bad_rows.csv"   # rows present in CSV but missing in your parsed result
DUCKDB_FILE    = r"D:/Darshana/Projects/Fifth_third/HMDA_Risk_Insights/db/hmda_risk.duckdb"   # optional persistence for ad-hoc SQL
SCHEMA_NAME    = "hmda"
TABLE_NAME     = "loan_applications"
# ======================================

os.makedirs(os.path.dirname(PARQUET_PATH), exist_ok=True)
os.makedirs(os.path.dirname(BAD_ROWS_PATH), exist_ok=True)

if not os.path.exists(CSV_PATH):
    raise FileNotFoundError(f"CSV not found: {CSV_PATH}")

con = duckdb.connect(DUCKDB_FILE)  # keep a persistent DB so you can inspect later
print(f"Connected to DuckDB: {DUCKDB_FILE}")

# 1) LOSSLESS READ (all columns as strings). This should NOT drop rows.
#    ALL_VARCHAR=TRUE + SAMPLE_SIZE=-1 avoids type inference and samples entire file.
con.execute(f"""
    CREATE OR REPLACE VIEW v_csv_all AS
    SELECT *
    FROM read_csv_auto('{CSV_PATH}',
                       ALL_VARCHAR=TRUE,
                       SAMPLE_SIZE=-1,
                       IGNORE_ERRORS=FALSE);
""")

# Count rows as read verbatim (string-only)
csv_all_cnt = con.execute("SELECT COUNT(*) FROM v_csv_all").fetchone()[0]
print(f"[1/5] Lossless (string) read count: {csv_all_cnt:,}")

# 2) PARSED READ (mimics earlier conversion). If you previously used IGNORE_ERRORS=TRUE,
#    rows that don't parse cleanly will be dropped here.
con.execute(f"""
    CREATE OR REPLACE VIEW v_csv_parsed AS
    SELECT *
    FROM read_csv_auto('{CSV_PATH}',
                       -- adjust formats if you know your date/timestamp patterns:
                       DATEFORMAT='%Y-%m-%d',
                       TIMESTAMPFORMAT='%Y-%m-%d %H:%M:%S',
                       IGNORE_ERRORS=TRUE);
""")

parsed_cnt = con.execute("SELECT COUNT(*) FROM v_csv_parsed").fetchone()[0]
print(f"[2/5] Parsed (auto-typed, ignore errors) count: {parsed_cnt:,}")

# 3) Build a column list dynamically from the lossless view to compare apples-to-apples.
#    We'll cast the parsed view's columns to VARCHAR and compare row-wise using EXCEPT.
cols = [c[0] for c in con.execute("SELECT * FROM v_csv_all LIMIT 0").description]

# Some safety: ensure the parsed view has all these columns (header mismatches can happen)
parsed_cols = [c[0] for c in con.execute("SELECT * FROM v_csv_parsed LIMIT 0").description]
common_cols = [c for c in cols if c in parsed_cols]
if not common_cols:
    raise RuntimeError("No common columns found between v_csv_all and v_csv_parsed. "
                       "Check header row / delimiter / quoting issues.")

col_list_all   = ", ".join([f'"{c}"' for c in common_cols])
col_list_cast  = ", ".join([f'CAST("{c}" AS VARCHAR)' for c in common_cols])

# 4) Identify the rows that were dropped by the parsed pipeline
#    "Bad rows" = present in lossless read, absent from parsed read
bad_rows_df = con.execute(f"""
    SELECT {col_list_all}
    FROM v_csv_all
    EXCEPT
    SELECT {col_list_cast}
    FROM v_csv_parsed
""").fetchdf()

bad_cnt = len(bad_rows_df)
print(f"[3/5] Rows present in CSV but missing after parsed read: {bad_cnt:,}")

# Save bad rows for inspection
if bad_cnt > 0:
    bad_rows_df.to_csv(BAD_ROWS_PATH, index=False, encoding="utf-8")
    print(f"[4/5] Saved dropped rows to: {BAD_ROWS_PATH}")
else:
    print("[4/5] No dropped rows detected with current settings.")

# 5) WRITE PARQUET WITHOUT LOSING ROWS
#    We write from the lossless view (all strings) so no rows are discarded.
#    This guarantees the parquet has the same row count as the original CSV.
con.execute(f"""
    COPY (
      SELECT * FROM v_csv_all
    ) TO '{PARQUET_PATH}'
    (FORMAT 'parquet', COMPRESSION 'zstd');
""")
print(f"[5/5] Wrote Parquet (no-loss) to: {PARQUET_PATH}")

# OPTIONAL: Create a physical table inside DuckDB from the no-loss parquet (so you can query later)
con.execute(f"CREATE SCHEMA IF NOT EXISTS {SCHEMA_NAME};")
con.execute(f"DROP TABLE IF EXISTS {SCHEMA_NAME}.{TABLE_NAME};")
con.execute(f"""
    CREATE TABLE {SCHEMA_NAME}.{TABLE_NAME} AS
    SELECT * FROM read_parquet('{PARQUET_PATH}');
""")

# Summary
persisted_cnt = con.execute(f"SELECT COUNT(*) FROM {SCHEMA_NAME}.{TABLE_NAME}").fetchone()[0]
print("\n=== SUMMARY ===")
print(f"CSV rows (lossless):        {csv_all_cnt:,}")
print(f"Parsed rows (ignore errs):  {parsed_cnt:,}")
print(f"Dropped rows detected:      {bad_cnt:,}")
print(f"DuckDB table rows:          {persisted_cnt:,}")
print(f"Done at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
