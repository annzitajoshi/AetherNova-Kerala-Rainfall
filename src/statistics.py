"""
AetherNova – Kerala Rainfall Trend Detective
NASA Space Apps Challenge 2026: Be an Earth System Trend Detective

Module: src/statistics.py
Description: Statistical analysis engine for climate trend detection, seasonal decomposition,
and anomaly estimation using pyMannKendall and SciPy.
"""

import calendar
from typing import Dict, List, Optional, Tuple
import numpy as np
import pandas as pd
import pymannkendall as mk
from scipy import stats

EXPECTED_ANNUAL_COLUMNS = [
    "year",
    "annual_rainfall_mm",
    "annual_rainfall_unweighted_mm",
    "months_present",
    "baseline_mean_mm",
    "anomaly_mm",
    "anomaly_pct",
    "rolling_avg_3yr",
]

EXPECTED_SEASONAL_COLUMNS = [
    "year",
    "season",
    "seasonal_rainfall_mm",
    "months_count",
]

EXPECTED_CLIMATOLOGY_COLUMNS = [
    "month",
    "month_name",
    "season",
    "mean_mm",
    "median_mm",
    "std_mm",
    "min_mm",
    "max_mm",
    "sample_count",
]


def compute_annual_totals(monthly_df: pd.DataFrame, min_months: int = 12) -> pd.DataFrame:
    """
    Aggregates monthly rainfall to annual totals for complete calendar years.
    Filters out years with fewer than `min_months` records.
    Guarantees a DataFrame with named expected columns is always returned.
    """
    if monthly_df is None or monthly_df.empty or "year" not in monthly_df.columns:
        return pd.DataFrame(columns=EXPECTED_ANNUAL_COLUMNS)

    col_weighted = (
        "rainfall_mm_weighted"
        if "rainfall_mm_weighted" in monthly_df.columns
        else ("rainfall_mm" if "rainfall_mm" in monthly_df.columns else None)
    )
    col_unweighted = (
        "rainfall_mm_unweighted"
        if "rainfall_mm_unweighted" in monthly_df.columns
        else col_weighted
    )

    if col_weighted is None:
        return pd.DataFrame(columns=EXPECTED_ANNUAL_COLUMNS)

    annual_records = []
    for yr, group in monthly_df.groupby("year"):
        if len(group) >= min_months:
            total_weighted = group[col_weighted].sum()
            total_unweighted = (
                group[col_unweighted].sum() if col_unweighted else total_weighted
            )
            annual_records.append({
                "year": int(yr),
                "annual_rainfall_mm": round(float(total_weighted), 2),
                "annual_rainfall_unweighted_mm": round(float(total_unweighted), 2),
                "months_present": len(group),
            })

    if not annual_records:
        return pd.DataFrame(columns=EXPECTED_ANNUAL_COLUMNS)

    df_annual = pd.DataFrame(annual_records)
    # Calculate baseline mean across available full years
    baseline_mean = df_annual["annual_rainfall_mm"].mean()
    df_annual["baseline_mean_mm"] = round(baseline_mean, 2)
    df_annual["anomaly_mm"] = (df_annual["annual_rainfall_mm"] - baseline_mean).round(2)
    df_annual["anomaly_pct"] = (
        ((df_annual["anomaly_mm"] / baseline_mean) * 100).round(2)
        if baseline_mean > 0
        else 0.0
    )
    df_annual["rolling_avg_3yr"] = (
        df_annual["annual_rainfall_mm"].rolling(window=3, min_periods=1).mean().round(2)
    )

    return df_annual


def compute_seasonal_breakdown(monthly_df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregates rainfall across Kerala's 4 meteorological seasons per year:
    - Southwest Monsoon (Edavappathi): Jun, Jul, Aug, Sep
    - Northeast Monsoon (Thulavarsham): Oct, Nov
    - Winter: Dec, Jan, Feb
    - Summer / Pre-Monsoon: Mar, Apr, May
    Guarantees a DataFrame with named expected columns is always returned.
    """
    if monthly_df is None or monthly_df.empty or "year" not in monthly_df.columns or "season" not in monthly_df.columns:
        return pd.DataFrame(columns=EXPECTED_SEASONAL_COLUMNS)

    col_weighted = (
        "rainfall_mm_weighted"
        if "rainfall_mm_weighted" in monthly_df.columns
        else ("rainfall_mm" if "rainfall_mm" in monthly_df.columns else None)
    )
    if col_weighted is None:
        return pd.DataFrame(columns=EXPECTED_SEASONAL_COLUMNS)

    seasonal_records = []
    for (yr, season), group in monthly_df.groupby(["year", "season"]):
        total_rain = group[col_weighted].sum()
        seasonal_records.append({
            "year": int(yr),
            "season": season,
            "seasonal_rainfall_mm": round(float(total_rain), 2),
            "months_count": len(group),
        })

    if not seasonal_records:
        return pd.DataFrame(columns=EXPECTED_SEASONAL_COLUMNS)

    df_seasonal = pd.DataFrame(seasonal_records)
    return df_seasonal


def run_mann_kendall_test(series: np.ndarray, alpha: float = 0.05) -> Dict:
    """
    Executes the non-parametric Mann-Kendall trend test with Sen's slope estimator.
    Args:
        series: 1D array of annual or seasonal rainfall totals.
        alpha: significance threshold (default: 0.05 for 95% confidence).
    Returns:
        Dictionary containing trend, p-value, z-statistic, Tau, Sen's slope, and interpretation.
    """
    if len(series) < 4:
        return {
            "status": "INSUFFICIENT_DATA",
            "message": "At least 4-5 complete years required to run statistical trend tests.",
            "trend": "no trend",
            "p": 1.0,
            "slope": 0.0,
            "tau": 0.0,
            "h": False,
        }

    res = mk.original_test(series, alpha=alpha)

    # Secondary linear regression for comparison
    x = np.arange(len(series))
    lr = stats.linregress(x, series)

    return {
        "status": "COMPUTED",
        "trend": res.trend,          # 'increasing', 'decreasing', 'no trend'
        "h": bool(res.h),            # True if statistically significant at alpha
        "p": float(round(res.p, 4)),
        "z": float(round(res.z, 4)),
        "tau": float(round(res.Tau, 4)),
        "sen_slope": float(round(res.slope, 2)),
        "intercept": float(round(res.intercept, 2)),
        "linreg_slope": float(round(lr.slope, 2)),
        "linreg_r2": float(round(lr.rvalue ** 2, 4)),
        "is_significant": bool(res.p < alpha),
    }


def compute_monthly_climatology(monthly_df: pd.DataFrame) -> pd.DataFrame:
    """Computes mean, median, min, and max rainfall for each calendar month."""
    if monthly_df is None or monthly_df.empty or "month" not in monthly_df.columns:
        return pd.DataFrame(columns=EXPECTED_CLIMATOLOGY_COLUMNS)

    col_weighted = (
        "rainfall_mm_weighted"
        if "rainfall_mm_weighted" in monthly_df.columns
        else ("rainfall_mm" if "rainfall_mm" in monthly_df.columns else None)
    )
    if col_weighted is None:
        return pd.DataFrame(columns=EXPECTED_CLIMATOLOGY_COLUMNS)

    climatology = []
    for month_num in range(1, 13):
        m_subset = monthly_df[monthly_df["month"] == month_num]
        if not m_subset.empty:
            month_name = (
                m_subset["month_name"].iloc[0]
                if "month_name" in m_subset.columns
                else calendar.month_abbr[month_num]
            )
            season_val = m_subset["season"].iloc[0] if "season" in m_subset.columns else "N/A"
            climatology.append({
                "month": month_num,
                "month_name": month_name,
                "season": season_val,
                "mean_mm": round(float(m_subset[col_weighted].mean()), 2),
                "median_mm": round(float(m_subset[col_weighted].median()), 2),
                "std_mm": round(float(m_subset[col_weighted].std()), 2) if len(m_subset) > 1 else 0.0,
                "min_mm": round(float(m_subset[col_weighted].min()), 2),
                "max_mm": round(float(m_subset[col_weighted].max()), 2),
                "sample_count": len(m_subset),
            })

    if not climatology:
        return pd.DataFrame(columns=EXPECTED_CLIMATOLOGY_COLUMNS)

    return pd.DataFrame(climatology)
