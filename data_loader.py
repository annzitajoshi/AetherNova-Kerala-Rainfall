"""
AetherNova – Kerala Rainfall Trend Detective
NASA Space Apps Challenge 2026: Be an Earth System Trend Detective

Module: src/data_loader.py
Description: Data access and caching layer supporting both authentic NASA GPM IMERG data
and synthetic multi-decadal prototype data.
"""

import json
from pathlib import Path
from typing import Dict, Tuple
import numpy as np
import pandas as pd
import streamlit as st


@st.cache_data
def load_nasa_gpm_data() -> pd.DataFrame:
    """Loads the authentic processed NASA GPM IMERG V07 monthly dataset (2018-2024)."""
    csv_path = Path(__file__).resolve().parent.parent / "data" / "processed" / "kerala_state_monthly_nasa_gpm.csv"
    if not csv_path.exists():
        # Fallback to test sample if main file not present
        csv_path = Path(__file__).resolve().parent.parent / "data" / "processed" / "kerala_monthly_test_sample.csv"

    df = pd.read_csv(csv_path)
    return df


@st.cache_data
def load_synthetic_demo_data() -> pd.DataFrame:
    """
    Generates synthetic multi-decadal monthly rainfall data for Kerala (2000-2024).
    IMPORTANT: This dataset is strictly for prototype demonstration of 25-year statistical
    trend detection algorithms prior to full multi-decadal satellite ingestion.
    """
    years = np.arange(2000, 2025)
    np.random.seed(42)

    records = []
    # Climatological monthly base distribution for Kerala (in mm)
    monthly_base = {
        1: (15.0, "Winter"),
        2: (25.0, "Winter"),
        3: (45.0, "Summer / Pre-Monsoon"),
        4: (115.0, "Summer / Pre-Monsoon"),
        5: (260.0, "Summer / Pre-Monsoon"),
        6: (620.0, "Southwest Monsoon (Edavappathi)"),
        7: (650.0, "Southwest Monsoon (Edavappathi)"),
        8: (420.0, "Southwest Monsoon (Edavappathi)"),
        9: (260.0, "Southwest Monsoon (Edavappathi)"),
        10: (300.0, "Northeast Monsoon (Thulavarsham)"),
        11: (180.0, "Northeast Monsoon (Thulavarsham)"),
        12: (40.0, "Winter"),
    }
    month_names = {
        1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun",
        7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"
    }

    for y in years:
        # Slight multi-decadal synthetic variation
        year_factor = 1.0 + np.random.normal(0.0, 0.12)
        if y == 2018:
            year_factor = 1.28  # Simulated 2018 flood peak
        elif y == 2016:
            year_factor = 0.72  # Simulated 2016 drought

        for m in range(1, 13):
            base_m, season = monthly_base[m]
            noise = np.random.normal(1.0, 0.18)
            rain_m = max(0.5, round(base_m * year_factor * noise, 2))
            records.append({
                "year": int(y),
                "month": int(m),
                "month_name": month_names[m],
                "season": season,
                "rainfall_mm_weighted": rain_m,
                "rainfall_mm_unweighted": rain_m,
                "data_source": "Prototype Synthetic Model (2000-2024)",
            })

    return pd.DataFrame(records)


@st.cache_data
def load_kerala_geojson() -> Dict:
    """Loads the verified Kerala boundary GeoJSON."""
    geojson_path = Path(__file__).resolve().parent.parent / "assets" / "geojson" / "kerala_boundary.geojson"
    with open(geojson_path, "r", encoding="utf-8") as f:
        return json.load(f)


@st.cache_data
def load_pixel_validation_data() -> pd.DataFrame:
    """Loads the 320 terrestrial pixel validation dataset."""
    csv_path = Path(__file__).resolve().parent.parent / "data" / "processed" / "june_2024_kerala_pixels_validation.csv"
    if csv_path.exists():
        return pd.read_csv(csv_path)
    return pd.DataFrame()
