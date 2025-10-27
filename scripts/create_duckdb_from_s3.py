import duckdb
import os
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

# Fetch credentials from environment
aws_region = os.getenv("AWS_REGION")
aws_key = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret = os.getenv("AWS_SECRET_ACCESS_KEY")

print("🔹 AWS Region:", aws_region)
print("🔹 Access Key Found:", bool(aws_key))
print("🔹 Secret Key Found:", bool(aws_secret))

# Connect to DuckDB
con = duckdb.connect("hmda_risk.duckdb")

# Configure S3 settings
con.execute(f"SET s3_region='{aws_region}'")
con.execute("SET s3_use_ssl=true")
con.execute("SET s3_url_style='path'")
con.execute(f"SET s3_access_key_id='{aws_key}'")
con.execute(f"SET s3_secret_access_key='{aws_secret}'")

# Read parquet from S3
s3_path = "s3://hmda-bucket/processed/loan_applications.parquet"  # use your real bucket
con.execute("""
    CREATE SCHEMA IF NOT EXISTS hmda;
    CREATE OR REPLACE TABLE hmda.loan_applications AS
    SELECT * FROM read_parquet($1);
""", [s3_path])

print("✅ Table created from S3 Parquet")

# Quick check
print(con.execute("SELECT COUNT(*) FROM hmda.loan_applications").fetchall())
