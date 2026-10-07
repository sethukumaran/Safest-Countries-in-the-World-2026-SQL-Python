"""
Safest Countries in the World 2026 — EDA + Business Analysis
Run:
    pip install -r requirements.txt
    python python/analysis.py

The script performs data quality checks, EDA, rankings, trend analysis,
correlations and exports analytical tables/visualizations.
"""

from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "safest-countries-in-the-world-2026.csv"
OUT = ROOT / "visualizations"
OUT.mkdir(exist_ok=True)

df = pd.read_csv(DATA)

# ---------- EDA / Data Quality ----------
print("Shape:", df.shape)
print("\nDtypes:\n", df.dtypes)
print("\nMissing values:\n", df.isna().sum())
print("\nDuplicate rows:", df.duplicated().sum())
print("Duplicate countries:", df["country"].duplicated().sum())
print("\nRisk distribution:\n", df["RiskLevelByCountryViaTravelSafe"].value_counts(dropna=False))

numeric = df.select_dtypes("number")
print("\nDescriptive statistics:\n", numeric.describe().T)

# ---------- Business Rankings ----------
print("\nTop 10 countries by 2026 GPI (lower is better):")
print(df[["country","GlobalPeaceIndex_2026"]].dropna()
      .sort_values("GlobalPeaceIndex_2026").head(10).to_string(index=False))

print("\nLowest terrorism index 2025 (lower is better):")
print(df[["country","GlobalTerrorismIndex_2025"]].dropna()
      .sort_values("GlobalTerrorismIndex_2025").head(10).to_string(index=False))

print("\nTop 10 TravelSafe index (higher is safer):")
print(df[["country","SafestCountriesIndexViaTravelSafe"]].dropna()
      .sort_values("SafestCountriesIndexViaTravelSafe", ascending=False).head(10).to_string(index=False))

print("\nTop 10 US News safety ranks (lower rank is better):")
print(df[["country","SafestCountriesRankUSNews_2024"]].dropna()
      .sort_values("SafestCountriesRankUSNews_2024").head(10).to_string(index=False))

# ---------- GPI change 2021 -> 2026 ----------
change = df.dropna(subset=["GlobalPeaceIndex_2021","GlobalPeaceIndex_2026"]).copy()
change["gpi_change"] = change["GlobalPeaceIndex_2026"] - change["GlobalPeaceIndex_2021"]
print("\nLargest GPI improvements (negative change = improvement):")
print(change[["country","GlobalPeaceIndex_2021","GlobalPeaceIndex_2026","gpi_change"]]
      .sort_values("gpi_change").head(10).to_string(index=False))

print("\nLargest GPI deteriorations:")
print(change[["country","GlobalPeaceIndex_2021","GlobalPeaceIndex_2026","gpi_change"]]
      .sort_values("gpi_change", ascending=False).head(10).to_string(index=False))

# ---------- Risk segment profile ----------
risk = df.groupby("RiskLevelByCountryViaTravelSafe").agg(
    countries=("country","count"),
    avg_gpi_2026=("GlobalPeaceIndex_2026","mean"),
    avg_gti_2025=("GlobalTerrorismIndex_2025","mean"),
    avg_travelsafe=("SafestCountriesIndexViaTravelSafe","mean"),
    avg_usnews_rank=("SafestCountriesRankUSNews_2024","mean")
).round(3)
print("\nRisk segment profile:\n", risk)

# ---------- Correlation ----------
corr = numeric.corr()
print("\nCorrelation matrix:\n", corr.round(2))

# ---------- Visualizations ----------
plt.rcParams.update({"figure.figsize": (10,6), "axes.titlesize": 14})

top = df[["country","GlobalPeaceIndex_2026"]].dropna().sort_values("GlobalPeaceIndex_2026").head(10).sort_values("GlobalPeaceIndex_2026", ascending=True)
plt.figure()
plt.barh(top["country"], top["GlobalPeaceIndex_2026"])
plt.xlabel("Global Peace Index 2026 (lower is better)")
plt.title("Top 10 Countries by Global Peace Index 2026")
plt.tight_layout()
plt.savefig(OUT/"01_top10_gpi_2026.png", dpi=180)
plt.close()

risk_counts = df["RiskLevelByCountryViaTravelSafe"].value_counts().reindex(["Low","Medium","High"]).dropna()
plt.figure()
plt.bar(risk_counts.index, risk_counts.values)
plt.ylabel("Number of countries")
plt.title("Countries by TravelSafe Risk Level")
plt.tight_layout()
plt.savefig(OUT/"02_risk_distribution.png", dpi=180)
plt.close()

gpi_years = [2021,2022,2023,2024,2025,2026]
gpi_means = [df[f"GlobalPeaceIndex_{y}"].mean() for y in gpi_years]
plt.figure()
plt.plot(gpi_years, gpi_means, marker="o")
plt.xticks(gpi_years)
plt.ylabel("Average GPI (lower is better)")
plt.xlabel("Year")
plt.title("Average Global Peace Index Trend, 2021–2026")
plt.tight_layout()
plt.savefig(OUT/"03_gpi_trend.png", dpi=180)
plt.close()

gti_years = [2022,2023,2024,2025]
gti_means = [df[f"GlobalTerrorismIndex_{y}"].mean() for y in gti_years]
plt.figure()
plt.plot(gti_years, gti_means, marker="o")
plt.xticks(gti_years)
plt.ylabel("Average GTI (lower is better)")
plt.xlabel("Year")
plt.title("Average Global Terrorism Index Trend, 2022–2025")
plt.tight_layout()
plt.savefig(OUT/"04_gti_trend.png", dpi=180)
plt.close()

scatter = df[["GlobalPeaceIndex_2026","SafestCountriesIndexViaTravelSafe"]].dropna()
plt.figure()
plt.scatter(scatter["GlobalPeaceIndex_2026"], scatter["SafestCountriesIndexViaTravelSafe"], alpha=.7)
plt.xlabel("GPI 2026 (lower is better)")
plt.ylabel("TravelSafe index (higher is safer)")
plt.title("Peace vs Travel Safety")
plt.tight_layout()
plt.savefig(OUT/"05_gpi_vs_travelsafe.png", dpi=180)
plt.close()

scatter = df[["GlobalPeaceIndex_2026","SafestCountriesRankUSNews_2024"]].dropna()
plt.figure()
plt.scatter(scatter["GlobalPeaceIndex_2026"], scatter["SafestCountriesRankUSNews_2024"], alpha=.7)
plt.xlabel("GPI 2026 (lower is better)")
plt.ylabel("US News safety rank (lower is better)")
plt.title("Global Peace Index vs US News Safety Rank")
plt.tight_layout()
plt.savefig(OUT/"06_gpi_vs_usnews.png", dpi=180)
plt.close()

improve = change.sort_values("gpi_change").head(10).sort_values("gpi_change", ascending=True)
plt.figure()
plt.barh(improve["country"], improve["gpi_change"])
plt.axvline(0, linewidth=1)
plt.xlabel("Change in GPI, 2021 → 2026 (negative = improvement)")
plt.title("Largest GPI Improvements")
plt.tight_layout()
plt.savefig(OUT/"07_gpi_improvements.png", dpi=180)
plt.close()

worse = change.sort_values("gpi_change", ascending=False).head(10).sort_values("gpi_change", ascending=False)
plt.figure()
plt.barh(worse["country"], worse["gpi_change"])
plt.axvline(0, linewidth=1)
plt.xlabel("Change in GPI, 2021 → 2026 (positive = deterioration)")
plt.title("Largest GPI Deteriorations")
plt.tight_layout()
plt.savefig(OUT/"08_gpi_deteriorations.png", dpi=180)
plt.close()

print("\nAnalysis completed. Charts saved in:", OUT)
