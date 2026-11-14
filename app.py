"""
AetherNova – Kerala Rainfall Trend Detective
Tagline: Decoding Rainfall. Discovering Patterns.
NASA Space Apps Challenge 2026: Be an Earth System Trend Detective

Main Streamlit Application Dashboard
Supports both Authentic NASA GPM IMERG observations (2018-2024) and
Multi-Decadal Prototype Synthetic mode (2000-2024).
"""

from pathlib import Path
import numpy as np
import pandas as pd
import streamlit as st

# Internal AetherNova modules
from src.data_loader import (
    load_kerala_geojson,
    load_nasa_gpm_data,
    load_pixel_validation_data,
    load_synthetic_demo_data,
)
from src.statistics import (
    compute_annual_totals,
    compute_monthly_climatology,
    compute_seasonal_breakdown,
    run_mann_kendall_test,
)
from src.visualizer import (
    plot_annual_rainfall,
    plot_kerala_spatial_map,
    plot_monthly_climatology_chart,
    plot_rainfall_anomalies,
    plot_seasonal_distribution,
)

# -----------------------------------------------------------------------------
# 1. Page Configuration
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="AetherNova – Decoding Rainfall. Discovering Patterns.",
    page_icon="🛰️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------------------------------------------------------
# 2. Inject Custom CSS
# -----------------------------------------------------------------------------
def load_custom_css():
    """Reads and injects the custom CSS file for modern dark navy styling."""
    css_path = Path(__file__).resolve().parent / "assets" / "css" / "style.css"
    if css_path.exists():
        with open(css_path, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_custom_css()

# -----------------------------------------------------------------------------
# 3. Sidebar Navigation & Data Mode Selector
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown('<div class="sidebar-brand-title">🛰️ AETHERNOVA</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-brand-tagline">Decoding Rainfall. Discovering Patterns.</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-brand-sub">Kerala Rainfall Trend Detective</div>', unsafe_allow_html=True)

    st.markdown(
        '<span class="badge-nasa">NASA Space Apps 2026</span>',
        unsafe_allow_html=True,
    )

    st.markdown("---")
    st.markdown("### 🎛️ Data Source Engine")
    data_mode = st.radio(
        label="Select Data Source:",
        options=[
            "🛰️ Authentic NASA GPM IMERG (2018–2024)",
            "🧪 Prototype Multi-Decadal Demo (2000–2024)",
        ],
        index=0,
    )

    is_real_data = "Authentic NASA" in data_mode

    # Load appropriate dataset
    if is_real_data:
        monthly_raw = load_nasa_gpm_data()
        mode_badge = '<span style="color: #10B981; font-weight: 600;">● LIVE NASA DATA</span>'
        data_title_tag = "[NASA GPM IMERG V07]"
    else:
        monthly_raw = load_synthetic_demo_data()
        mode_badge = '<span style="color: #FBBF24; font-weight: 600;">● DEMO PROTOTYPE MODE</span>'
        data_title_tag = "[SYNTHETIC DEMO MODEL]"

    st.markdown("---")
    st.markdown("### 🧭 Navigation")
    nav_selection = st.radio(
        label="Select View:",
        options=[
            "🏠 Home (Overview)",
            "📈 Long-term Trends",
            "🌦️ Seasonal Patterns",
            "🗺️ Spatial / District View",
            "ℹ️ Mission & Methodology",
        ],
        index=0,
        label_visibility="collapsed",
    )

    st.markdown("---")
    st.markdown("### ⚙️ Temporal Filter")
    avail_years = (
        sorted(monthly_raw["year"].unique())
        if ("year" in monthly_raw.columns and not monthly_raw.empty)
        else [2024]
    )
    min_yr = int(avail_years[0])
    max_yr = int(avail_years[-1])
    if min_yr == max_yr:
        year_range = (min_yr, max_yr)
        st.markdown(f"**Calendar Year:** `{min_yr}`")
    else:
        year_range = st.slider(
            "Filter Calendar Years:",
            min_value=min_yr,
            max_value=max_yr,
            value=(min_yr, max_yr),
            step=1,
        )

    st.markdown(
        f"""
        <div class="sidebar-status-box">
            <b>Status:</b> {mode_badge}<br>
            <b>Coverage:</b> {year_range[0]}–{year_range[1]}<br>
            <b>Spatial Mask:</b> 320 Terrestrial Cells<br>
            <b>Area-Weighted:</b> Cosine Latitude ($w = \\cos\\phi$)
        </div>
        """,
        unsafe_allow_html=True,
    )

# Filter monthly data by selected year range
if not monthly_raw.empty and "year" in monthly_raw.columns:
    filtered_monthly = monthly_raw[
        (monthly_raw["year"] >= year_range[0]) & (monthly_raw["year"] <= year_range[1])
    ]
else:
    filtered_monthly = pd.DataFrame()

annual_data = compute_annual_totals(filtered_monthly)
seasonal_data = compute_seasonal_breakdown(filtered_monthly)
climatology_data = compute_monthly_climatology(filtered_monthly)

# Run Mann-Kendall test
if not annual_data.empty and len(annual_data) >= 4 and "annual_rainfall_mm" in annual_data.columns:
    mk_results = run_mann_kendall_test(annual_data["annual_rainfall_mm"].values)
else:
    mk_results = {
        "status": "INSUFFICIENT_DATA",
        "trend": "no trend",
        "p": 1.0,
        "tau": 0.0,
        "sen_slope": 0.0,
        "intercept": 0.0,
        "linreg_r2": 0.0,
        "is_significant": False,
    }

# -----------------------------------------------------------------------------
# 4. View Rendering
# -----------------------------------------------------------------------------

# --- VIEW 1: HOME (OVERVIEW) ---
if nav_selection == "🏠 Home (Overview)":
    st.markdown(
        """
        <div class="hero-container">
            <div class="hero-top-meta">
                <span class="badge-nasa">NASA Space Apps 2026</span>
                <span class="badge-track">Earth System Trend Detective</span>
            </div>
            <div class="hero-title">AetherNova</div>
            <div class="hero-tagline">Decoding Rainfall. Discovering Patterns.</div>
            <div class="hero-subtitle">
                An interactive Earth science intelligence platform investigating historical multi-decadal precipitation dynamics, 
                monsoon shifts, and rainfall anomalies across Kerala, India, powered by authentic NASA satellite observations.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not is_real_data:
        st.markdown(
            """
            <div class="demo-alert-banner">
                <span>⚠️</span>
                <div>
                    <strong>Prototype Mode Active:</strong> You are currently viewing 
                    <strong>Synthetic Multi-Decadal Demo Data (2000–2024)</strong>. 
                    Switch to <em>'Authentic NASA GPM IMERG'</em> in the sidebar to view verified NASA satellite observations.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            """
            <div style="background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.35); color: #34D399; padding: 0.75rem 1.25rem; border-radius: 8px; font-size: 0.88rem; margin-bottom: 1.5rem;">
                <strong>Authentic Satellite Data Verified:</strong> Displaying terrestrial observations from 
                <strong>NASA GPM IMERG V07 Final Run</strong> calibrated across 320 boundary-masked Kerala grid cells.
            </div>
            """,
            unsafe_allow_html=True,
        )

    # 4 Key Summary Metric Cards
    m1, m2, m3, m4 = st.columns(4)

    has_annual = (
        not annual_data.empty
        and "annual_rainfall_mm" in annual_data.columns
        and len(annual_data) > 0
    )
    base_mean = float(annual_data["annual_rainfall_mm"].mean()) if has_annual else 0.0

    has_season = (
        not seasonal_data.empty
        and "season" in seasonal_data.columns
        and "seasonal_rainfall_mm" in seasonal_data.columns
    )
    if has_season:
        sw_group = seasonal_data[seasonal_data["season"].str.contains("Southwest", na=False)]
        sw_mean = float(sw_group["seasonal_rainfall_mm"].mean()) if not sw_group.empty else 0.0
    else:
        sw_mean = 0.0
    sw_share = (sw_mean / base_mean * 100) if base_mean > 0 else 0.0

    max_yr_row = annual_data.loc[annual_data["annual_rainfall_mm"].idxmax()] if has_annual else None

    with m1:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">Mean Annual Rainfall</div>
                <div class="metric-value">{base_mean:.1f} <span style="font-size: 1rem; color: #94A3B8;">mm</span></div>
                <div class="metric-sub">Period: {year_range[0]}–{year_range[1]}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with m2:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">SW Monsoon Share</div>
                <div class="metric-value">{sw_share:.1f} <span style="font-size: 1rem; color: #94A3B8;">%</span></div>
                <div class="metric-sub">Mean: {sw_mean:.1f} mm (Jun–Sep)</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with m3:
        slope_val = mk_results.get("sen_slope", 0.0)
        p_val = mk_results.get("p", 1.0)
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">Sen's Trend Slope</div>
                <div class="metric-value" style="color: {'#10B981' if slope_val >= 0 else '#38BDF8'};">{slope_val:+.1f} <span style="font-size: 1rem; color: #94A3B8;">mm/yr</span></div>
                <div class="metric-sub">p-value: {p_val:.3f} ({mk_results.get('trend', 'no trend')})</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with m4:
        if max_yr_row is not None and "year" in max_yr_row and "annual_rainfall_mm" in max_yr_row:
            st.markdown(
                f"""
                <div class="metric-card">
                <div class="metric-label">Max Recorded Peak Year</div>
                <div class="metric-value" style="color: #00F0FF;">{max_yr_row['annual_rainfall_mm']:.0f} <span style="font-size: 1rem; color: #94A3B8;">mm</span></div>
                <div class="metric-sub">Observed Year: {int(max_yr_row['year'])}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                """
                <div class="metric-card">
                <div class="metric-label">Max Recorded Peak Year</div>
                <div class="metric-value" style="color: #94A3B8;">N/A</div>
                <div class="metric-sub">No complete annual records</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.write("")

    # Annual rainfall Plotly chart
    if annual_data.empty or "year" not in annual_data.columns or len(annual_data) == 0:
        st.warning(
            "⚠️ **Annual Rainfall Totals Unavailable:** Complete 12-month calendar year observations "
            "are not available for the selected temporal filter or data source. "
            "Full annual totals require 12 complete monthly observations per calendar year to prevent seasonal distortion."
        )
    else:
        fig_annual = plot_annual_rainfall(
            annual_data,
            title_suffix=data_title_tag,
            trend_slope=mk_results.get("sen_slope") if mk_results.get("status") == "COMPUTED" else None,
            trend_intercept=mk_results.get("intercept") if mk_results.get("status") == "COMPUTED" else None,
        )
        st.markdown('<div class="chart-box">', unsafe_allow_html=True)
        st.plotly_chart(fig_annual, width="stretch")
        st.markdown("</div>", unsafe_allow_html=True)

    # Scientific Pillars
    st.markdown("### 🔬 Scientific Investigation Pillars")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(
            """
            <div class="feature-card">
                <h4>🛰️ Calibrated Satellite Observations</h4>
                <p>
                    Extracts high-resolution precipitation fields from <strong>NASA GPM IMERG V07 Final Run</strong> 
                    at 0.1° (~10 km) resolution, calibrated with ground gauge networks worldwide.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            """
            <div class="feature-card">
                <h4>📊 Non-Parametric Trend Detection</h4>
                <p>
                    Deploys the <strong>Mann-Kendall test</strong> and <strong>Sen's Slope Estimator</strong> 
                    to evaluate climate trajectories resilient to extreme outlier precipitation years.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c3:
        st.markdown(
            """
            <div class="feature-card">
                <h4>🗺️ Land-Boundary Masking</h4>
                <p>
                    Filters exactly 320 terrestrial grid points via <strong>geoBoundaries ADM1</strong> 
                    point-in-polygon clipping, completely removing coastal Arabian Sea distortion.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )


# --- VIEW 2: LONG-TERM TRENDS ---
elif nav_selection == "📈 Long-term Trends":
    st.markdown("## 📈 Statistical Trend Detection & Anomaly Analysis")
    st.markdown(f"**Data Engine:** `{data_title_tag}` | **Coverage:** `{year_range[0]}–{year_range[1]}`")

    if is_real_data:
        st.info("ℹ️ **NASA Historical Data Note:** You are inspecting 7 full years (2018–2024) of authentic NASA observations. A minimum of 4-5 years enables trend detection; 20+ years is optimal for climate normals.")

    # Statistical Trend Table Cards
    t1, t2, t3, t4 = st.columns(4)
    with t1:
        st.metric("Mann-Kendall Trend", mk_results.get("trend", "N/A").title())
    with t2:
        st.metric("p-value (alpha=0.05)", f"{mk_results.get('p', 1.0):.4f}")
    with t3:
        st.metric("Sen's Slope", f"{mk_results.get('sen_slope', 0.0):+.2f} mm/yr")
    with t4:
        st.metric("Kendall's Tau", f"{mk_results.get('tau', 0.0):+.3f}")

    # Anomaly Chart
    if not annual_data.empty and len(annual_data) > 0 and "anomaly_pct" in annual_data.columns:
        fig_anom = plot_rainfall_anomalies(annual_data, title_suffix=data_title_tag)
        st.markdown('<div class="chart-box">', unsafe_allow_html=True)
        st.plotly_chart(fig_anom, width="stretch")
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.warning(
            "⚠️ **Annual Anomalies Unavailable:** Complete annual baseline totals could not be computed for this temporal filter. "
            "At least 4 complete calendar years (12 months each) are required for statistical trend and anomaly estimation."
        )

    # Annual Data Table
    with st.expander("📋 View Annual Rainfall & Anomaly Data Table", expanded=False):
        if not annual_data.empty and len(annual_data) > 0:
            st.dataframe(annual_data, width="stretch", hide_index=True)
        else:
            st.info("No complete annual records available to display in table.")


# --- VIEW 3: SEASONAL PATTERNS ---
elif nav_selection == "🌦️ Seasonal Patterns":
    st.markdown("## 🌦️ Seasonal Rainfall Dynamics & Climatology")
    st.markdown(f"**Data Engine:** `{data_title_tag}` | **Coverage:** `{year_range[0]}–{year_range[1]}`")

    c_left, c_right = st.columns([3, 2])

    with c_left:
        if not seasonal_data.empty and len(seasonal_data) > 0 and "seasonal_rainfall_mm" in seasonal_data.columns:
            fig_season = plot_seasonal_distribution(seasonal_data, title_suffix=data_title_tag)
            st.plotly_chart(fig_season, width="stretch")
        else:
            st.info("No seasonal records available for the selected criteria.")

    with c_right:
        if not climatology_data.empty and len(climatology_data) > 0 and "mean_mm" in climatology_data.columns:
            fig_clim = plot_monthly_climatology_chart(climatology_data, title_suffix=data_title_tag)
            st.plotly_chart(fig_clim, width="stretch")
        else:
            st.info("No climatology records available for the selected criteria.")

    st.markdown("### 📊 Climatological Monthly Distribution")
    if not climatology_data.empty and len(climatology_data) > 0:
        st.dataframe(climatology_data, width="stretch", hide_index=True)
    else:
        st.info("No monthly climatological distribution records available.")


# --- VIEW 4: SPATIAL / DISTRICT VIEW ---
elif nav_selection == "🗺️ Spatial / District View":
    st.markdown("## 🗺️ Spatial Satellite Grid & Terrestrial Validation")
    st.markdown("Visualizing the 320 terrestrial satellite pixels strictly inside Kerala's boundary.")

    pixel_df = load_pixel_validation_data()
    if not pixel_df.empty:
        fig_map = plot_kerala_spatial_map(pixel_df, month_label="June 2024 (Verified NASA Granule)")
        st.plotly_chart(fig_map, width="stretch")

        s1, s2, s3, s4 = st.columns(4)
        with s1:
            st.metric("Total Terrestrial Cells", f"{len(pixel_df)}")
        with s2:
            st.metric("Mean Pixel Rainfall", f"{pixel_df['rainfall_mm'].mean():.1f} mm")
        with s3:
            st.metric("Min Grid Cell", f"{pixel_df['rainfall_mm'].min():.1f} mm")
        with s4:
            st.metric("Max Grid Cell", f"{pixel_df['rainfall_mm'].max():.1f} mm")

        with st.expander("📍 Inspect Terrestrial Grid Coordinates & Rain Rates", expanded=False):
            st.dataframe(pixel_df, width="stretch", hide_index=True)
    else:
        st.warning("Pixel validation dataset not found. Please verify data/processed/ directory.")


# --- VIEW 5: MISSION & METHODOLOGY ---
elif nav_selection == "ℹ️ Mission & Methodology":
    st.markdown("## ℹ️ Mission, Data Provenance & Methodology")
    st.markdown(
        """
        ### NASA Space Apps Challenge 2026: Be an Earth System Trend Detective
        * **Project:** AetherNova – Kerala Rainfall Trend Detective
        * **Tagline:** Decoding Rainfall. Discovering Patterns.
        * **Primary Target Dataset:** NASA GPM IMERG Final Precipitation L3 1 Month 0.1° x 0.1° V07 (`GPM_3IMERGM_07`)
        * **Data Provider:** NASA Goddard Earth Sciences Data and Information Services Center (GES DISC) / Earthdata Cloud
        * **Land Boundary Source:** `geoBoundaries gbOpen` (IND ADM1 - Kerala), CC BY 2.5 IN
        * **Temporal Integration Formula:** $\\text{Rainfall (mm)} = \\text{precipitation (mm/hr)} \\times \\text{hours in month}$
        * **Spatial Masking:** 320 grid cells centered within Kerala's terrestrial polygon, weighted by $\\cos(\\text{latitude})$.
        
        ---
        ### 👥 Team AetherNova
        * **Annzita Joshi** – Team Lead, Development, Data Analysis & UI/UX
        * **Ashna Maria Saji** – NASA Dataset Research, Literature & Documentation Support
        
        ---
        ### 📑 June 2024 Scientific Validation Audit Summary
        * **NASA GPM IMERG Calculated (Kerala Terrestrial):** `404.00 mm`
        * **IMD Official Reference (Kerala & Mahe Subdivision):** `489.30 mm`
        * **Discrepancy:** `-85.30 mm (-17.43%)`
        * **Methodological Distinction:** NASA GPM IMERG is a spaceborne microwave-infrared gridded reanalysis product over a Kerala-only polygon. IMD utilizes surface rain gauge interpolation across the Kerala & Mahe meteorological subdivision. Satellite sensors experience orographic warm-rain undercatch over the steep Western Ghats. NASA data is independent and is not calibrated to IMD regional networks.
        """
    )

# -----------------------------------------------------------------------------
# 5. Application Footer
# -----------------------------------------------------------------------------
st.markdown(
    """
    <div class="footer-text">
        <strong>AetherNova</strong> – <em>Decoding Rainfall. Discovering Patterns.</em> | NASA Space Apps Challenge 2026<br>
        Kerala Rainfall Trend Detective • Developed by Annzita Joshi & Ashna Maria Saji
    </div>
    """,
    unsafe_allow_html=True,
)
