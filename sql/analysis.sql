-- ====================================
-- HMDA Data Analysis Queries
-- Author: Darshana
-- ====================================

-- 🟡 1. Peek at first 20 rows
SELECT *
FROM hmda.loan_applications
LIMIT 20;

-- 🧮 2. Count total rows in the table
SELECT COUNT(*) AS total_rows
FROM hmda.loan_applications;

-- 📅 3. Distribution by activity year
SELECT activity_year, COUNT(*) AS row_count
FROM hmda.loan_applications
GROUP BY activity_year
ORDER BY activity_year;

-- 🗺️ 4. Top 10 states by number of applications
SELECT state_code, COUNT(*) AS total_applications
FROM hmda.loan_applications
GROUP BY state_code
ORDER BY total_applications DESC
LIMIT 10;

-- 💰 5. Loan amount summary statistics
SELECT 
    MIN(loan_amount) AS min_loan,
    MAX(loan_amount) AS max_loan,
    AVG(loan_amount) AS avg_loan,
    MEDIAN(loan_amount) AS median_loan
FROM hmda.loan_applications;

-- 👤 6. Count distinct LEIs (unique institutions)
SELECT COUNT(DISTINCT lei) AS unique_leis
FROM hmda.loan_applications;

-- 🧼 7. Check missing values in key columns
SELECT
    SUM(CASE WHEN lei IS NULL OR TRIM(lei) = '' THEN 1 ELSE 0 END) AS missing_lei,
    SUM(CASE WHEN state_code IS NULL OR TRIM(state_code) = '' THEN 1 ELSE 0 END) AS missing_state,
    SUM(CASE WHEN loan_amount IS NULL THEN 1 ELSE 0 END) AS missing_loan_amount
FROM hmda.loan_applications;

-- ✨ Add more analytical queries below as needed
