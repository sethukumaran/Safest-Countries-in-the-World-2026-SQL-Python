# Safest-Countries-in-the-World-2026-SQL-Python

## 1. Project Overview
This project performs a senior-level exploratory and business-oriented analysis of the **Safest Countries in the World 2026** dataset using **Python (Pandas + NumPy + Matplotlib)** and **SQL**.
The analysis evaluates:
- Global Peace Index (GPI), 2021–2026
- Global Terrorism Index (GTI), 2022–2025
- TravelSafe country safety index
- TravelSafe risk classification
- US News safety ranking (2024)
The objective is to move beyond simple ranking and identify **data-quality issues, safety trends, cross-source consistency, risk segments, country-level improvements/deteriorations, and decision-useful business insights**.

## 2. Dataset Snapshot

- **Countries/rows:** 195
- **Columns:** 15
- **Duplicate rows:** 0
- **Duplicate country names:** 0
- **Countries with GPI 2026:** 163
- **Countries with GTI 2025:** 98
- **Countries with TravelSafe index:** 191
- **Countries with US News rank:** 89

### Important metric direction
- **GPI:** lower = more peaceful / safer.
- **GTI:** lower = lower terrorism impact.
- **TravelSafe index:** higher = safer.
- **US News safety rank:** lower numeric rank = better.

## 3. EDA / Data Quality Findings

### Completeness
The dataset has substantial source-coverage differences. GPI is available for roughly 163 countries, while GTI is available for fewer than 100 countries in the latest year. US News rank is available for only 89 countries.

This means **missingness is largely structural/source-coverage related**, not automatically evidence of poor data collection. Analyses should therefore avoid treating missing values as zero or as a safety score.

### Integrity
- No duplicate rows were found.
- No duplicate country names were found.
- Two countries are missing flag codes.
- Four countries are missing TravelSafe risk/index values.

## 4. Key Business Findings

### 4.1 Global peace trend
Average GPI changed from **2.083 in 2021** to **2.081 in 2026**.

The 2024 average was higher than 2023, followed by improvement in 2025 and 2026. This indicates that the overall global picture is **not a straight-line trend**; it contains year-to-year volatility.

### 4.2 Terrorism trend
Average GTI declined from **3.879 in 2022** to **2.880 in 2025**, based on the countries available in each year's GTI data.

Because GTI coverage changes materially by year, this trend should be interpreted as a **reported-sample trend**, not as a complete global census trend.

### 4.3 TravelSafe risk segmentation
The TravelSafe classification contains:
- **Low:** 86 countries
- **Medium:** 74 countries
- **High:** 31 countries

Average 2026 GPI by risk group:
- Low: 1.724
- Medium: 2.104
- High: 2.675

The segmentation is directionally coherent: the high-risk segment has a substantially worse peace profile than the low-risk segment.

### 4.4 Cross-source consistency
On the overlapping observations:
- GPI 2026 vs TravelSafe index correlation: **-0.78**
- GPI 2026 vs US News safety rank correlation: **+0.78**
- TravelSafe index vs US News rank correlation: **-0.76**

These signs are exactly what we would expect given the scoring directions. The strength of the relationships indicates **meaningful agreement between independent safety perspectives**, while not implying that the measures are interchangeable.

### 4.5 Countries with major GPI improvement
The largest 2021→2026 improvements (negative GPI change) include:
- Libya
- Iraq
- Afghanistan
- Zimbabwe
- Venezuela
- Lebanon
- Nicaragua
- Uzbekistan
- Yemen
- Philippines

These are **relative index movements**, not a statement that every country above is currently safe. A country can improve materially and still remain high-risk.

### 4.6 Countries with major deterioration
The largest increases in GPI include:
- Haiti
- Ukraine
- Ecuador
- Israel
- Myanmar
- Russia
- Burkina Faso
- Chad
- Sweden
- Palestine

These should be treated as **watch-list candidates** for further investigation into the drivers behind deterioration.

## 5. Top 2026 Peace Performers

The leading countries by 2026 GPI include:
1. Iceland
2. New Zealand
3. Switzerland
4. Slovenia
5. Ireland
6. Austria
7. Portugal
8. Singapore
9. Finland
10. Japan

The exact ranking is based on the supplied dataset and the GPI direction where lower is better.

## 6. Business Questions Answered

### Executive / Strategy
1. Which countries have the strongest peace scores?
2. Which countries have the lowest reported terrorism index?
3. Which countries score highest on TravelSafe safety?
4. Which countries have the best US News safety ranks?
5. Which countries improved or deteriorated most over 2021–2026?
6. Does TravelSafe risk segmentation align with peace and terrorism measures?
7. Do independent safety sources broadly agree?
8. Where are the strongest cross-source discrepancies or data gaps?

### Data / Analytics
1. How complete is each source?
2. Are there duplicates?
3. Which metrics are strongly correlated?
4. Are missing values concentrated in specific sources?
5. What is the direction of year-over-year movement?

## 7. Visualization Outputs

The `visualizations/` folder contains:

1. `01_top10_gpi_2026.png` — Top 10 peaceful countries
2. `02_risk_distribution.png` — TravelSafe risk distribution
3. `03_gpi_trend.png` — Average GPI trend
4. `04_gti_trend.png` — Average GTI trend
5. `05_gpi_vs_travelsafe.png` — Peace vs TravelSafe
6. `06_gpi_vs_usnews.png` — Peace vs US News rank
7. `07_gpi_improvements.png` — Largest GPI improvements
8. `08_gpi_deteriorations.png` — Largest GPI deteriorations

## 8. SQL Analysis

`sql/analysis_queries.sql` contains reusable queries for:
- Data quality checks
- Risk distribution
- Top-N rankings
- GPI movement
- Risk-segment profiling
- Annual trend analysis
- Cross-source screening

The SQL is written in a SQLite/DuckDB-friendly style.

## 9. Python Analysis

`python/analysis.py` performs:
- Initial EDA
- Schema and data-type checks
- Missing-value profiling
- Duplicate detection
- Descriptive statistics
- Business rankings
- GPI change analysis
- Risk segmentation
- Correlation analysis
- Visualization generation

## 10. Analytical Limitations

1. The dataset combines multiple source methodologies; their scores should not be interpreted as one common scale.
2. Missingness is substantial for GTI and US News, so cross-source comparisons use only overlapping records.
3. Correlation does not establish causation.
4. A country with a large improvement in GPI can still have a poor absolute safety level.
5. The supplied dataset should be treated as the analytical source of truth for this project; external validation would be required before making travel, investment, insurance, or policy decisions.

## 11. Conclusion

**The analysis shows that country safety is multidimensional, but the supplied measures exhibit strong directional agreement.** Countries classified as low risk by TravelSafe generally have better peace scores, lower terrorism-index values, stronger TravelSafe safety scores, and better US News rankings. The cross-source correlations are strong enough to support using multiple indicators together for screening, while still keeping the underlying methodologies separate.

From a decision-making perspective, the most important insight is that **absolute safety and improvement are different questions**. Countries such as Libya and Iraq show substantial improvement in GPI from 2021 to 2026, but improvement alone should not move them into a low-risk category. Conversely, deterioration in countries such as Haiti and Ukraine identifies areas that deserve monitoring even when a single ranking may not fully capture the change.

The dataset is therefore best used as a **country safety intelligence framework**: combine current peace level, terrorism exposure, travel-risk classification, and independent rankings; explicitly account for missing data; and monitor changes over time rather than relying on a single league table.


