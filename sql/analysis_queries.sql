-- Safest Countries in the World 2026
-- SQLite/DuckDB-style analytical SQL.
-- Import the CSV into a table named safest_countries before running.

-- 1. Data quality profile
SELECT
    COUNT(*) AS total_rows,
    COUNT(DISTINCT country) AS distinct_countries,
    SUM(CASE WHEN flagCode IS NULL THEN 1 ELSE 0 END) AS missing_flag_codes,
    SUM(CASE WHEN GlobalPeaceIndex_2026 IS NULL THEN 1 ELSE 0 END) AS missing_gpi_2026,
    SUM(CASE WHEN GlobalTerrorismIndex_2025 IS NULL THEN 1 ELSE 0 END) AS missing_gti_2025,
    SUM(CASE WHEN SafestCountriesIndexViaTravelSafe IS NULL THEN 1 ELSE 0 END) AS missing_travelsafe,
    SUM(CASE WHEN SafestCountriesRankUSNews_2024 IS NULL THEN 1 ELSE 0 END) AS missing_usnews
FROM safest_countries;

-- 2. Risk-level distribution
SELECT
    RiskLevelByCountryViaTravelSafe AS risk_level,
    COUNT(*) AS countries,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) AS pct_of_dataset
FROM safest_countries
GROUP BY RiskLevelByCountryViaTravelSafe
ORDER BY countries DESC;

-- 3. Top 10 peaceful countries in 2026 (lower GPI is better)
SELECT country, GlobalPeaceIndex_2026
FROM safest_countries
WHERE GlobalPeaceIndex_2026 IS NOT NULL
ORDER BY GlobalPeaceIndex_2026 ASC
LIMIT 10;

-- 4. Top 10 lowest-terrorism countries in 2025 (lower GTI is better)
SELECT country, GlobalTerrorismIndex_2025
FROM safest_countries
WHERE GlobalTerrorismIndex_2025 IS NOT NULL
ORDER BY GlobalTerrorismIndex_2025 ASC
LIMIT 10;

-- 5. Top 10 TravelSafe countries (higher index is better)
SELECT country, SafestCountriesIndexViaTravelSafe
FROM safest_countries
WHERE SafestCountriesIndexViaTravelSafe IS NOT NULL
ORDER BY SafestCountriesIndexViaTravelSafe DESC
LIMIT 10;

-- 6. Top 10 US News safety ranks (lower rank is better)
SELECT country, SafestCountriesRankUSNews_2024
FROM safest_countries
WHERE SafestCountriesRankUSNews_2024 IS NOT NULL
ORDER BY SafestCountriesRankUSNews_2024 ASC
LIMIT 10;

-- 7. GPI change from 2021 to 2026
-- Negative change = improvement because lower GPI is better.
SELECT
    country,
    GlobalPeaceIndex_2021,
    GlobalPeaceIndex_2026,
    ROUND(GlobalPeaceIndex_2026 - GlobalPeaceIndex_2021, 3) AS gpi_change
FROM safest_countries
WHERE GlobalPeaceIndex_2021 IS NOT NULL
  AND GlobalPeaceIndex_2026 IS NOT NULL
ORDER BY gpi_change ASC
LIMIT 10;

-- 8. Largest GPI deteriorations
SELECT
    country,
    GlobalPeaceIndex_2021,
    GlobalPeaceIndex_2026,
    ROUND(GlobalPeaceIndex_2026 - GlobalPeaceIndex_2021, 3) AS gpi_change
FROM safest_countries
WHERE GlobalPeaceIndex_2021 IS NOT NULL
  AND GlobalPeaceIndex_2026 IS NOT NULL
ORDER BY gpi_change DESC
LIMIT 10;

-- 9. Risk segment business profile
SELECT
    RiskLevelByCountryViaTravelSafe AS risk_level,
    COUNT(*) AS countries,
    ROUND(AVG(GlobalPeaceIndex_2026), 3) AS avg_gpi_2026,
    ROUND(AVG(GlobalTerrorismIndex_2025), 3) AS avg_gti_2025,
    ROUND(AVG(SafestCountriesIndexViaTravelSafe), 3) AS avg_travelsafe,
    ROUND(AVG(SafestCountriesRankUSNews_2024), 3) AS avg_usnews_rank
FROM safest_countries
GROUP BY RiskLevelByCountryViaTravelSafe
ORDER BY
    CASE RiskLevelByCountryViaTravelSafe
        WHEN 'Low' THEN 1
        WHEN 'Medium' THEN 2
        WHEN 'High' THEN 3
        ELSE 4
    END;

-- 10. Annual GPI trend
SELECT 2021 AS year, AVG(GlobalPeaceIndex_2021) AS avg_gpi FROM safest_countries
UNION ALL SELECT 2022, AVG(GlobalPeaceIndex_2022) FROM safest_countries
UNION ALL SELECT 2023, AVG(GlobalPeaceIndex_2023) FROM safest_countries
UNION ALL SELECT 2024, AVG(GlobalPeaceIndex_2024) FROM safest_countries
UNION ALL SELECT 2025, AVG(GlobalPeaceIndex_2025) FROM safest_countries
UNION ALL SELECT 2026, AVG(GlobalPeaceIndex_2026) FROM safest_countries
ORDER BY year;

-- 11. Annual terrorism trend
SELECT 2022 AS year, AVG(GlobalTerrorismIndex_2022) AS avg_gti FROM safest_countries
UNION ALL SELECT 2023, AVG(GlobalTerrorismIndex_2023) FROM safest_countries
UNION ALL SELECT 2024, AVG(GlobalTerrorismIndex_2024) FROM safest_countries
UNION ALL SELECT 2025, AVG(GlobalTerrorismIndex_2025) FROM safest_countries
ORDER BY year;

-- 12. Countries appearing strong across multiple safety measures.
-- This is a simple business screening rule, not an official composite score.
SELECT
    country,
    GlobalPeaceIndex_2026,
    GlobalTerrorismIndex_2025,
    SafestCountriesIndexViaTravelSafe,
    SafestCountriesRankUSNews_2024
FROM safest_countries
WHERE GlobalPeaceIndex_2026 <= 1.6
  AND GlobalTerrorismIndex_2025 <= 1.0
  AND SafestCountriesIndexViaTravelSafe >= 80
ORDER BY GlobalPeaceIndex_2026 ASC;
