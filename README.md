# 🏦 Home Mortgage Lending – Risk & Strategy Insights (2019–2024)

**Why this project:** I’ve always been fascinated by how financial data shapes a bank’s pricing, risk appetite, and growth decisions. To explore this in a practical way, I analyzed public mortgage application data from the **Home Mortgage Disclosure Act (HMDA)**, focusing on **Fifth Third Bank** to keep the insights directly relevant to a Risk & Strategy role.

---

## Client Background

**Fifth Third Bank** is a large U.S. financial institution with a broad retail footprint across multiple states. Like all regulated lenders, Fifth Third reports mortgage application data to the FFIEC under HMDA. This provides a transparent view of application volumes, approvals/denials, borrower and property characteristics, and several credit risk indicators.

Using HMDA filings for **2019–2024**, I built an end-to-end analysis to surface the kinds of signals a Risk & Strategy team monitors: approval trends, denial drivers, risk levers (DTI/CLTV), pricing dispersion, product/channel mix, and geographic concentrations.

> **Note:** This analysis uses public data for learning and demonstration only; it is not affiliated with Fifth Third Bank.

---

## North Star Metrics

- **Applications** – total mortgage applications received  
- **Approvals & Approval Rate** – originations as a share of applications  
- **Risk Mix** – % with **DTI > 43** and **CLTV > 95**  
- **Pricing Signals** – average **interest rate**, **rate spread**, presence of **discount points** or **lender credits**  
- **Denial Drivers** – distribution of **top denial reasons**  
- **Geographic View** – approval rate and risk mix by **state/county**

---

## Executive Summary (2019–2024)

**Portfolio & Trend**
- Applications and approval rates show clear **year-over-year variation**, with noticeable normalization post-pandemic highs.
- **Approval Rate** trend highlights sensitivity to product mix and risk levers over time.

**Risk Indicators**
- Pockets of **elevated CLTV (>95%)** and **high DTI (>43)** appear in specific geographies and loan purposes, suggesting areas for tighter policy calibration.
- **Rate spread** dispersion and **special feature flags** (balloon, interest-only) are limited but useful for pricing governance.

**Denial Analytics**
- A small set of **denial reasons** explains most adverse decisions; their mix shifts by state and product, indicating targeted process or policy opportunities.

**Actionable Takeaways**
- Use **state × product** views to refine pricing and risk cutoffs where risk mix is consistently higher.
- Track **denial mix** and **rework rates** to reduce friction in borderline segments.
- Monitor **DTI/CLTV bands** alongside approval rate to maintain portfolio quality through cycles.

> <img width="1547" height="874" alt="image" src="https://github.com/user-attachments/assets/a3de5821-d681-42d2-8957-e43052fdb420" />


---

## Dataset Structure & Data Model (ERD)

**Source:** HMDA Public LAR (Loan/Application Register), FFIEC/CFPB  
**Years Covered:** 2019–2024  
**Grain:** one application/loan record (annual reporting)

**Star Schema (Power BI)**
- **Fact:** `Loan_Application_Fact` (application-level numerics: loan amount, interest rate, costs/fees, DTI/CLTV, etc.)
- **Dimensions:**  
  - `Date_Dim` (activity year)  
  - `Location_Dim` (state, county, census tract)  
  - `Borrower_Dim` (age, sex, race, ethnicity)  
  - `Loan_Product_Dim` (loan type & purpose)  
  - `Property_Dim` (occupancy, construction method, units)  
  - `Lender_Dim` (purchaser type)  
  - `Action_Dim` (action taken)  
  - `Mortgage_Dim` (lien, HOEPA)  
  - `Credit_Dim` (credit scoring model)  
  - `Denial_Dim` (primary denial reason)

> <img width="2133" height="1141" alt="data_model" src="https://github.com/user-attachments/assets/0769ae3d-23f2-4c16-a113-9a9c4342c8dc" />


---

## Insights Deep-Dive

### 1) Approval & Volume
- **Approval Rate** by year and product shows periods of tightening/loosening credit.
- Product lines with consistently **below-average approval** warrant policy or funnel review.

### 2) Risk Levers (DTI & CLTV)
- **High DTI % (>43)** and **High CLTV % (>95)** by **state** and **loan purpose** reveal risk concentrations.
- Pair these with approval rate to detect **adverse selection** (high approvals where risk is elevated).

### 3) Pricing & Fees
- **Rate Spread** distribution by year indicates pricing dispersion; outliers merit governance review.
- **Discount Points** and **Lender Credits** prevalence helps validate pricing practices and customer segmentation.

### 4) Denial Reasons
- Top reasons (e.g., **Debt-to-Income ratio**, **Credit history**) differ by geography and product; this steers **targeted remediation** (e.g., documentation guidance, pre-qualification changes).

### 5) Geography
- **State-level heatmaps** highlight where approval softens and high-risk metrics cluster—useful for regional strategy and capacity planning.

---

> <img width="1545" height="874" alt="image" src="https://github.com/user-attachments/assets/aec6949f-8534-42ab-9dee-d426d9345ebb" />

> <img width="1546" height="874" alt="image" src="https://github.com/user-attachments/assets/df9d3807-4b6f-4155-9ed0-adc2f91e06d7" />

> <img width="1546" height="874" alt="image" src="https://github.com/user-attachments/assets/901a5b41-7c43-4200-921b-e39fec859e6a" />


---

## What This Enables for a Risk & Strategy Team

- **Early risk detection:** rising DTI/CLTV pockets or weakening approvals by region/product  
- **Policy calibration:** align cutoffs and documentation to reduce avoidable denials  
- **Pricing governance:** monitor spread dispersion and fee usage across cycles  
- **Geographic strategy:** concentrate outreach where approval likelihood and risk mix are favorable

---

## How to Reproduce

1. **Data**  
   - Download HMDA LAR (2019–2024) from the FFIEC/CFPB site.  
   - Filter rows to Fifth Third Bank (by **LEI**).  

2. **Processing**  
   - Clean & standardize (Excel/Python).  
   - Convert to **Parquet** and store in **S3** (optional).  

3. **Modeling**  
   - Load into SQL Server (or DuckDB), create star schema (fact + dimensions).  
   - Import into **Power BI**, connect relationships, and add DAX measures.

4. **Reporting**  
   - Open the Power BI file and refresh.  
   - Adjust slicers to explore year, state, product, and borrower segments.

> Minimal tech stack: **Excel / Python / Parquet / S3 / SQL Server / Power BI (DAX)**

---

## Key Measures (DAX Highlights)

- **Applications**, **Approved**, **Approval Rate**  
- **High DTI % (>43)**, **High CLTV % (>95)**  
- **Avg Interest Rate**, **Rate Spread ≥ 1.5%**, **% with Discount Points / Lender Credits**  
- **Denial Rate** and **Top Denial Reasons**  
- **Parity ratios** for exploratory fair-lending slices (e.g., Approval vs. reference group)

*(See `/powerbi/measures.md` for the full list.)*

---

## Recommendations

- **Monitor** approval + risk mix together (DTI/CLTV vs Approval Rate) at the **state × product** level.  
- **Target** denial-heavy segments with **pre-qualification guidance** or **documentation checklists**.  
- **Govern** pricing dispersion with periodic **rate spread** and **fee** reviews.  
- **Plan** market strategy using geographic hot spots where approval and risk mix are favorable.

---

## Disclaimer

This project is for educational and portfolio purposes. It is **not** affiliated with Fifth Third Bank. All data is sourced from the **public HMDA dataset**.

---
