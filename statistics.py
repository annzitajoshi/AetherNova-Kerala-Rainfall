"""
AetherNova – Kerala Rainfall Trend Detective
NASA Space Apps Challenge 2026: Be an Earth System Trend Detective

Module: src/statistics.py
Description: Statistical analysis engine for climate trend detection, seasonal decomposition,
and anomaly estimation using pyMannKendall and SciPy.
"""

from typing import Dict, Tuple
import numpy as np
import pandas as pd
import pymannkendall as mk
from scipy import stats


def compute_annual_totals(monthly_df: pd.DataFrame, min_months: int = 12) -> pd.DataFrame:
    """
    Aggregates monthly rainfall to annual totals for complete calendar years.
    Filters out years with fewer than `min_months` records.
    """
    annual_records = []
    for yr, group in monthly_df.groupby("year"):
        if len(group) >= min_months:
            total_weighted = group["rainfall_mm_weighted"].sum()
            total_unweighted = group["rainfall_mm_unweighted"].sum()
            annual_records.append({
                "year": int(yr),
                "annual_rainfall_mm": round(float(total_weighted), 2),
                "annual_rainfall_unweighted_mm": round(float(total_unweighted), 2),
                "months_present": len(group),
            })

    df_annual = pd.DataFrame(annual_records)
    if not df_annual.empty:
        # Calculate baseline mean across available full years
        baseline_mean = df_annual["annual_rainfall_mm"].mean()
        df_annual["baseline_mean_mm"] = round(baseline_mean, 2)
        df_annual["anomaly_mm"] = (df_annual["annual_rainfall_mm"] - baseline_mean).round(2)
        df_annual["anomaly_pct"] = ((df_annual["anomaly_mm"] / baseline_mean) * 100).round(2)
        df_annual["rolling_avg_3yr"] = df_annual["annual_rainfall_mm"].rolling(window=3, min_periods=1).mean().round(2)

    return df_annual


def compute_seasonal_breakdown(monthly_df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregates rainfall across Kerala's 4 meteorological seasons per year:
    - Southwest Monsoon (Edavappathi): Jun, Jul, Aug, Sep
    - Northeast Monsoon (Thulavarsham): Oct, Nov
    - Winter: Dec, Jan, Feb
    - Summer / Pre-Monsoon: Mar, Apr, May
    """
    seasonal_records = []
    for (yr, season), group in monthly_df.groupby(["year", "season"]):
        total_rain = group["rainfall_mm_weighted"].sum()
        seasonal_records.append({
            "year": int(yr),
            "season": season,
            "seasonal_rainfall_mm": round(float(total_rain), 2),
            "months_count": len(group),
        })

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
    climatology = []
    for month_num in range(1, 13):
        m_subset = monthly_df[monthly_df["month"] == month_num]
        if not m_subset.empty:
            climatology.append({
                "month": month_num,
                "month_name": m_subset["month_name"].iloc[0],
                "season": m_subset["season"].iloc[0],
                "mean_mm": round(float(m_subset["rainfall_mm_weighted"].mean()), 2),
                "median_mm": round(float(m_subset["rainfall_mm_weighted"].median()), 2),
                "std_mm": round(float(m_subset["rainfall_mm_weighted"].std()), 2) if len(m_subset) > 1 else 0.0,
                "min_mm": round(float(m_subset["rainfall_mm_weighted"].min()), 2),
                "max_mm": round(float(m_subset["rainfall_mm_weighted"].max()), 2),
                "sample_count": len(m_subset),
            })
    return pd.DataFrame(climatology)
