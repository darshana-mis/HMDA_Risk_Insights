-- ============================================
-- HMDA table inspection (DuckDB-compatible SQL)
-- ============================================
-- Adjust schema/table names if yours differ:
--   schema: hmda
--   table : loan_applications

-- 0) Schemas & tables (use information_schema for compatibility)
SELECT schema_name
FROM information_schema.schemata
ORDER BY schema_name;

SELECT table_schema, table_name
FROM information_schema.tables
WHERE table_schema = 'hmda'
ORDER BY table_name;

-- 1) Structure
DESCRIBE hmda.loan_applications;

-- 2) Quick peek
SELECT *
FROM hmda.loan_applications
LIMIT 20;

-- 3) Row count
SELECT COUNT(*) AS total_rows
FROM hmda.loan_applications;

-- 4) Distinct counts for some key columns (edit as needed)
SELECT 
  COUNT(DISTINCT lei)           AS distinct_lei,
  COUNT(DISTINCT activity_year) AS distinct_activity_year,
  COUNT(DISTINCT state_code)    AS distinct_state_code,
  COUNT(DISTINCT county_code)   AS distinct_county_code,
  COUNT(DISTINCT action_taken)  AS distinct_action_taken
FROM hmda.loan_applications;

-- 5) Year distribution
SELECT activity_year, COUNT(*) AS n_rows
FROM hmda.loan_applications
GROUP BY activity_year
ORDER BY activity_year;

-- 6) Top states by volume
SELECT state_code, COUNT(*) AS n_rows
FROM hmda.loan_applications
GROUP BY state_code
ORDER BY n_rows DESC
LIMIT 20;

-- 7) Missingness (NULL/empty %) for selected columns
WITH base AS (
  SELECT COUNT(*)::DOUBLE AS n
  FROM hmda.loan_applications
)
SELECT 'lei' AS column_name,
       (SUM(CASE WHEN lei IS NULL OR TRIM(CAST(lei AS VARCHAR)) = '' THEN 1 ELSE 0 END)::DOUBLE / n) * 100 AS null_pct
FROM hmda.loan_applications, base
UNION ALL
SELECT 'loan_amount',
       (SUM(CASE WHEN loan_amount IS NULL THEN 1 ELSE 0 END)::DOUBLE / n) * 100
FROM hmda.loan_applications, base
UNION ALL
SELECT 'state_code',
       (SUM(CASE WHEN state_code IS NULL OR TRIM(CAST(state_code AS VARCHAR)) = '' THEN 1 ELSE 0 END)::DOUBLE / n) * 100
FROM hmda.loan_applications, base
UNION ALL
SELECT 'applicant_age',
       (SUM(CASE WHEN applicant_age IS NULL THEN 1 ELSE 0 END)::DOUBLE / n) * 100
FROM hmda.loan_applications, base
ORDER BY null_pct DESC;

-- 8) Numeric summary for loan_amount (edit for other numerics)
SELECT 
  MIN(loan_amount)                        AS min_loan_amount,
  MAX(loan_amount)                        AS max_loan_amount,
  AVG(loan_amount)                        AS avg_loan_amount,
  MEDIAN(loan_amount)                     AS p50_loan_amount,
  QUANTILE(loan_amount, 0.25)             AS p25_loan_amount,
  QUANTILE(loan_amount, 0.75)             AS p75_loan_amount
FROM hmda.loan_applications;

-- 9) Common categories
SELECT action_taken, COUNT(*) AS n
FROM hmda.loan_applications
GROUP BY action_taken
ORDER BY n DESC
LIMIT 15;

SELECT loan_type, COUNT(*) AS n
FROM hmda.loan_applications
GROUP BY loan_type
ORDER BY n DESC
LIMIT 15;

SELECT loan_purpose, COUNT(*) AS n
FROM hmda.loan_applications
GROUP BY loan_purpose
ORDER BY n DESC
LIMIT 15;

-- 10) Exact duplicate rows (entire-row duplicates)
WITH total AS (
  SELECT COUNT(*) AS total_rows FROM hmda.loan_applications
),
dedup AS (
  SELECT COUNT(*) AS distinct_rows FROM (
    SELECT DISTINCT * FROM hmda.loan_applications
  )
)
SELECT 
  total_rows,
  distinct_rows,
  total_rows - distinct_rows AS exact_duplicate_rows
FROM total, dedup;

-- 11) "Business key" duplicate check (edit columns to your key)
SELECT 
  lei, activity_year, action_taken, COUNT(*) AS dup_count
FROM hmda.loan_applications
GROUP BY lei, activity_year, action_taken
HAVING COUNT(*) > 1
ORDER BY dup_count DESC, lei
LIMIT 100;

-- 12) Simple data quality checks
-- Empty strings in lei
SELECT COUNT(*) AS empty_lei_strings
FROM hmda.loan_applications
WHERE lei IS NULL OR TRIM(CAST(lei AS VARCHAR)) = '';

-- Non-positive loan amounts
SELECT COUNT(*) AS non_positive_loan_amounts
FROM hmda.loan_applications
WHERE loan_amount IS NOT NULL AND loan_amount <= 0;

-- 13) Final peek
SELECT * FROM hmda.loan_applications LIMIT 100;
