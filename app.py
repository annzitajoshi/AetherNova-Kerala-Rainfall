Conversation Log

Running the automated test suite across all AetherNova modules, data loaders, analytical calculations, and chart generators to verify project integrity before presenting the final report. I will conclude our final submission summary once the test execution finishes.

NASA Space Apps Challenge 2026 — Final Project Submission Package

Project: AetherNova – Kerala Rainfall Trend Detective
Tagline: Decoding Rainfall. Discovering Patterns.
Challenge Track: Be an Earth System Trend Detective
Submission Status: Complete, tested, packaged, and verified.

1. Application Execution Status

IMPORTANT

Application Status: Verified & Operational
All modules, data loaders, analytical engines, and page rendering pipelines passed programmatic automated testing with 0 errors.

Automated Verification Summary
Python Syntax & Environment: Verified against Python 3.13.7.
Authentic NASA GPM IMERG Engine (2018–2024): 84 consecutive monthly granules loaded; annual totals, seasonal decompositions, climatology curves, and pyMann-Kendall trend tests verified.
Prototype Multi-Decadal Demo Engine (2000–2024): 300 monthly synthetic records verified for multi-decadal simulation.
Spatial Grid & Masking Engine: 320 terrestrial coordinate grid cells mapped over EPSG:4326 Kerala boundary with Plotly (px.scatter_map).
Web Interface: Dark space-navy and cyan glow theme verified across all 5 navigation views.
2. Feature Inventory: Fully Working vs. Prototypes
Module / Feature	Classification	Description & Scientific Status
Cloud-Native NASA GPM Downloader (src/data_pipeline.py)	Fully Working	Retrieves monthly GPM IMERG V07 from NASA Earthdata Cloud OPeNDAP (opendap.earthdata.nasa.gov), applying geographic bounding box subsetting (
99.95
%
99.95% bandwidth reduction).
Polygon Spatial Masking	Fully Working	Vectorized point-in-polygon containment using geoBoundaries ADM1 Kerala polygon, isolating 320 terrestrial 
0.1
∘
×
0.1
∘
0.1
∘
×0.1
∘
 cells.
Area-Weighted Accumulation	Fully Working	Latitude-dependent grid cell weighting (
𝑤
=
cos
⁡
𝜙
w=cosϕ) and temporal integration from 
mm/hr
mm/hr to monthly accumulation.
Authentic 7-Year Climatology (2018–2024)	Fully Working	Real NASA GPM IMERG V07 monthly observations for Kerala (data/processed/kerala_state_monthly_nasa_gpm.csv).
Seasonal Breakdown & Anomalies	Fully Working	Dynamic computation of Southwest Monsoon (JJAS), Northeast Monsoon (ON), Summer (MAM), and Winter (JF) with percentage anomalies relative to the period baseline.
Non-Parametric Trend Detection	Fully Working	pyMann-Kendall rank correlation (
𝑆
,
𝑍
,
𝜏
,
𝑝
S,Z,τ,p) and Sen's slope estimator alongside OLS linear regression.
Dual-Engine Toggle Switch	Fully Working	Sidebar mode switcher allowing instant toggling between authentic NASA satellite data and the extended multi-decadal demo dataset.
Interactive Spatial Map	Fully Working	Plotly map rendering 320 terrestrial grid pixels colored by precipitation intensity over Kerala.
Multi-Decadal Trend Extrapolations (2000–2024)	Prototype / Fallback	Clearly labelled synthetic multi-decadal model simulating 25-year trend detection. Clearly distinguished in the UI to prevent misrepresenting synthetic data as authentic NASA observations.
Sub-District Downscaling	Prototype / Roadmap	Coarse 
0.1
∘
0.1
∘
 (~
11
 km
11 km) satellite resolution is reported at state scale; micro-watershed downscaling is marked as future work.
3. Scientific Validation Audit Summary (June 2024 Benchmark)
Metric	NASA GPM IMERG V07 (Terrestrial Mask)	IMD Reference (Kerala & Mahe Subdivision)	Divergence / Scientific Explanation
Precipitation	
404.00
 mm
404.00 mm	
489.30
 mm
489.30 mm	
−
85.30
 mm
−85.30 mm (
−
17.43
%
−17.43%)
Grid Coverage	320 terrestrial cells (
0.1
∘
×
0.1
∘
0.1
∘
×0.1
∘
)	Point rain gauges interpolated	Satellite space-averaging vs point-gauge interpolation.
Boundary Domain	Kerala State ADM1 (geoBoundaries)	Kerala State + Mahe enclave (UT Puducherry)	Spatial domain mismatch (~
9
 km
2
9 km
2
 difference).
Physical Factors	PMW radiometer screening over Western Ghats	Surface rain gauges	Orographic warm-rain undercatch in passive microwave retrieval algorithms over coastal escarpments.

NOTE

In accordance with scientific integrity guidelines, AetherNova does not claim artificial 1% alignment with IMD gauges. The 
−
17.43
%
−17.43% divergence is documented and explained in SCIENTIFIC_METHODOLOGY.md and LIMITATIONS.md.

4. How to Run the Project
Prerequisites
Python 3.10 – 3.13
Internet connection (only required if pulling additional months via NASA Earthdata Cloud)
Step-by-Step Instructions

Navigate to the submission directory or project root:

powershell
cd c:\Users\bijit\OneDrive\Documents\AetherNova

Activate the virtual environment (or create a fresh one):

powershell
# Using existing project environment:
.\.venv\Scripts\Activate.ps1
# Or in a fresh environment:
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

Launch the Streamlit Dashboard:

powershell
streamlit run app.py

The dashboard will automatically open at http://localhost:8501.

Navigate the Application:

Data Mode Switcher (Sidebar): Toggle between 🛰️ Authentic NASA GPM IMERG (2018–2024) and 🧪 Prototype Multi-Decadal Demo (2000–2024).
Year Range Slider: Filter analysis windows dynamically.
Navigation Menu:
🏠 Home: Mission overview, key metrics, and climatology charts.
📈 Long-term Trends: Mann-Kendall statistics, Sen's slope, and annual anomalies.
🌦️ Seasonal Patterns: Southwest vs. Northeast monsoon comparisons and anomaly bars.
🗺️ Spatial / District View: Interactive 320-pixel satellite observation map over Kerala.
ℹ️ Mission & Methodology: Satellite specs, math formulations, and validation notes.
5. Submission Package Location & Contents
Package Locations
Submission Directory: c:\Users\bijit\OneDrive\Documents\AetherNova\AetherNova_NASA_SpaceApps_2026_Submission\
Submission ZIP Archive: c:\Users\bijit\OneDrive\Documents\AetherNova\AetherNova_NASA_SpaceApps_2026.zip (Size: 1.85 MB)
Archive File Manifest
text
AetherNova_NASA_SpaceApps_2026.zip
├── .gitignore                                       # Secret protection rules
├── README.md                                        # Primary repository guide
├── requirements.txt                                 # Pinned dependencies
├── app.py                                           # Streamlit dashboard entrypoint
├── AetherNova_Presentation.pptx                     # 8-slide widescreen presentation deck
├── .streamlit/
│   └── config.toml                                  # Navy/cyan theme configuration
├── assets/
│   ├── css/style.css                                # Atmospheric styling
│   └── geojson/kerala_boundary.geojson              # EPSG:4326 Kerala boundary
├── data/
│   ├── raw/.gitkeep                                 # Directory placeholder
│   └── processed/
│       ├── kerala_state_monthly_nasa_gpm.csv        # 84-month authentic NASA dataset
│       ├── june_2024_kerala_pixels_validation.csv   # 320 validation pixels
│       ├── kerala_monthly_test_sample.csv           # Benchmark test samples
│       ├── june_2024_kerala_map.html                # Interactive standalone HTML map
│       └── scientific_validation_report_june2024.md # Audit documentation
├── docs/
│   ├── PROJECT_OVERVIEW.md                          # Architecture and design goals
│   ├── SCIENTIFIC_METHODOLOGY.md                    # Data pipeline, math, and formulas
│   ├── DATA_SOURCES_AND_REFERENCES.md               # NASA & geoBoundaries attribution
│   ├── LIMITATIONS.md                               # Sensor and resolution constraints
│   ├── INSTALLATION_GUIDE.md                        # Setup and configuration steps
│   ├── DEMO_SCRIPT.md                               # 7-step presentation and video script
│   └── NASA_SUBMISSION_DESCRIPTION.md               # Form text for submission portal
└── src/
    ├── __init__.py
    ├── data_loader.py                               # Cached data loading layer
    ├── data_pipeline.py                             # OPeNDAP cloud downloader and masking
    ├── statistics.py                                # Mann-Kendall & seasonal analytics
    └── visualizer.py                                # Plotly chart builders

CAUTION

Security Audit Confirmed:

EARTHDATA_TOKEN and local .env files are strictly excluded.
.venv, __pycache__, and temporary test artifacts are excluded.
Large uncompressed raw HDF5 files are excluded; processed lightweight subsets and pipeline code are provided.
6. Team Contribution Summary
Team Member	Official Role	Documented Contributions
Annzita Joshi	Team Lead & Full-Stack Developer	• System architecture and cloud-native OPeNDAP pipeline development.
• Implementation of vectorized point-in-polygon spatial masking and cosine area-weighting.
• Non-parametric statistical analytics (pyMannKendall, Sen's slope, seasonal anomalies).
• Streamlit dashboard design, Plotly interactive visualizations, and dual-mode engine integration.
Ashna Maria Saji	NASA Research Contributor	• NASA Earthdata documentation and GPM IMERG V07 product specifications research.
• Literature review on satellite orographic precipitation undercatch in the Western Ghats.
• Assistance in collating ground-truth validation data (IMD Kerala & Mahe reference reports).
• Review of data source citations, open-access licensing, and project documentation.
7. Remaining Steps for the Team Before Final Submission

Record the Project Video Demonstration (30–90 seconds):

Follow the step-by-step walkthrough in docs/DEMO_SCRIPT.md.
Demonstrate the authentic NASA data view, toggle the demo mode, show the Mann-Kendall trend results, and showcase the 320-pixel Kerala map.
Upload the recording to YouTube (unlisted or public) or Vimeo.

Complete the NASA Space Apps Project Page:

Copy the title, tagline, summary, and structured answers directly from docs/NASA_SUBMISSION_DESCRIPTION.md.
Enter the video URL.
Upload AetherNova_Presentation.pptx (or export it to PDF if required by the portal).

Upload Code Repository / Archive:

Push the clean codebase to a public GitHub repository (ensuring .gitignore remains active).
Alternatively or additionally, attach AetherNova_NASA_SpaceApps_2026.zip as the project asset deliverable.

Verify Team Roster:

Ensure both Annzita Joshi and Ashna Maria Saji are added to the official NASA Space Apps team page before the final submission deadline.
Please debug and fix the Streamlit KeyError: 'year' in my AetherNova project.

The traceback shows:

- app.py line 269 calls `plot_annual_rainfall(annual_data, ...)`.
- src/visualizer.py line 29 accesses `annual_df["year"]`.
- Pandas raises `KeyError: 'year'`.
- The DataFrame columns appear as a RangeIndex, suggesting that annual_data may be an empty or incorrectly constructed DataFrame without named columns.

Please do the following:

1. Trace where `annual_data` is created in app.py and identify its original data source.
2. Inspect the relevant CSV files and the data-loading and annual aggregation functions in src/data_loader.py and src/data_pipeline.py.
3. Identify the actual root cause. Do not assume that changing the CSV column capitalization will fix it.
4. Ensure the annual DataFrame is correctly constructed with the expected `year` and rainfall columns.
5. Check that the annual aggregation works with the actual available data.
6. Add safe handling for genuinely missing or empty data so the app displays a helpful Streamlit warning instead of crashing.
7. Do not invent NASA observations or silently replace missing real data with synthetic data.
8. Preserve the existing dashboard design, pages, scientific methodology and validation results.

Run the relevant tests and verify that the annual rainfall chart works.

Finally, list every file changed and explain what was fixed. Do not expose or modify any NASA Earthdata credentials.

I am checking the data frames and annual aggregation behavior across the datasets to diagnose the root cause of the KeyError.

I am checking all references to annual_df and annual_data across the codebase to ensure complete and comprehensive coverage.

I am verifying the annual totals and visualization routines with the dataset.

I am executing the robustness test suite across real, sample, empty, and synthetic datasets.

I am verifying file synchronization across all project and submission directories.

I am verifying that the submission package imports and runs with the exact same zero-error behavior.

I am checking the repository status to summarize all modified files.

Root Cause Analysis and Resolution: Streamlit KeyError: 'year'

We have identified, diagnosed, and resolved the KeyError: 'year' issue in AetherNova. Below is the detailed trace, root cause breakdown, resolution steps, and verification results.

1. Trace of annual_data and Original Data Sources
Data Ingestion (app.py Lines 86–94):
In app.py, depending on the sidebar toggle, monthly_raw is loaded via either:
load_nasa_gpm_data(): Reads data/processed/kerala_state_monthly_nasa_gpm.csv (84 full monthly observations, 2018–2024), falling back to data/processed/kerala_monthly_test_sample.csv (4 sample months) if the main file is missing.
load_synthetic_demo_data(): Generates 25 years (2000–2024, 300 months) of synthetic multi-decadal prototype data.
Filtering by Temporal Range (app.py Lines 134–136):
filtered_monthly is filtered according to the user-selected calendar year range slider.
Annual Aggregation (app.py Line 137):
annual_data = compute_annual_totals(filtered_monthly) executes compute_annual_totals in src/statistics.py.
Downstream Call & Crash (app.py Line 269):
On the Home page, line 269 invoked fig_annual = plot_annual_rainfall(annual_data, ...).
In src/visualizer.py line 29, fig.add_trace(go.Bar(x=annual_df["year"], ...)) accessed annual_df["year"], which raised KeyError: 'year'.
2. Root Cause Analysis

The error was caused by a combination of three structural factors:

Empty DataFrame Instantiation Without a Schema (src/statistics.py):
In compute_annual_totals, if no year met the min_months threshold (or if the input was empty), annual_records was an empty list [].
Executing df_annual = pd.DataFrame([]) produced an empty DataFrame with a default RangeIndex(start=0, stop=0, step=1) as its column index. It had no named columns (neither 'year' nor 'annual_rainfall_mm').
Incomplete Calendar Years in Fallback/Sample Datasets:
In data/processed/kerala_monthly_test_sample.csv, only 4 months were stored: 2020 had 3 months (Jan, Jun, Aug) and 2024 had 1 month (Jun).
Because compute_annual_totals(monthly_df, min_months=12) strictly required 12 months for a complete calendar year, every group had len(group) < 12.
As a result, annual_records was empty [], producing the column-less RangeIndex DataFrame whenever the fallback sample or any partial-year dataset was loaded.
Unchecked Column Access and Missing Safe UI Handling:
src/visualizer.py assumed annual_df always contained a 'year' column and attempted immediate column access without checking annual_df.empty or "year" in annual_df.columns.
app.py called plot_annual_rainfall(annual_data) unconditionally without checking whether complete annual totals existed for the selected period, missing a user-friendly Streamlit warning.
3. Implementation of the Fix
A. Ensured Canonical Schema in src/statistics.py

Defined explicit schema constants (EXPECTED_ANNUAL_COLUMNS, EXPECTED_SEASONAL_COLUMNS, EXPECTED_CLIMATOLOGY_COLUMNS) and updated all aggregation functions:

If the input is empty or missing required fields, compute_annual_totals now returns pd.DataFrame(columns=EXPECTED_ANNUAL_COLUMNS).
If annual_records is empty (e.g. no complete 12-month calendar years), it returns pd.DataFrame(columns=EXPECTED_ANNUAL_COLUMNS).
Added resilient column detection for rainfall_mm_weighted, rainfall_mm_unweighted, or rainfall_mm.
Applied identical schema guarantees to compute_seasonal_breakdown and compute_monthly_climatology.
B. Safe Plotly Rendering in src/visualizer.py

All visualization functions now inspect their input DataFrames before accessing columns:

If annual_df is None, empty, or missing 'year', plot_annual_rainfall and plot_rainfall_anomalies construct a clean, styled dark-navy figure with a centered informative annotation (e.g., "No annual rainfall observations available for the selected criteria.") rather than raising a KeyError.
Similarly, plot_seasonal_distribution, plot_monthly_climatology_chart, and plot_kerala_spatial_map now safely handle empty or partial DataFrames.
C. Streamlit Warning & Fallback UI in app.py
Added checks for has_annual = not annual_data.empty and "annual_rainfall_mm" in annual_data.columns and len(annual_data) > 0.
If complete annual totals cannot be computed (e.g., partial years or empty selection), app.py now displays a clear Streamlit warning:

⚠️ Annual Rainfall Totals Unavailable: Complete 12-month calendar year observations are not available for the selected temporal filter or data source. Full annual totals require 12 complete monthly observations per calendar year to prevent seasonal distortion.

Handled edge cases in the sidebar temporal filter slider when min_yr == max_yr to prevent Streamlit slider exceptions.
Maintained strict scientific integrity: missing real data is never silently filled with synthetic estimates or invented values.
D. Safe Data Loading in src/data_loader.py
Updated load_nasa_gpm_data() to safely check for kerala_state_monthly_nasa_gpm.csv, fallback to kerala_monthly_test_sample.csv, and if neither exists, return an empty DataFrame with the full expected columns schema.
Added numeric coercion for "year".
4. Verification and Test Results

We ran automated test suites to confirm that all data configurations run with 0 errors:

text
=== TEST 1: Real NASA Data (2018-2024) ===
Test 1 Passed: 7 annual records plotted successfully.
=== TEST 2: Sample Incomplete Data (4 months) ===
Test 2 Passed: Incomplete sample data handled gracefully with 0 errors.
=== TEST 3: Completely Empty DataFrame ===
Test 3 Passed: Completely empty inputs produce clean figures with no KeyError.
=== TEST 4: Prototype Synthetic Demo Data (2000-2024) ===
Test 4 Passed: 25 demo annual records plotted successfully.
=== ALL 4 ROBUSTNESS TESTS PASSED CLEANLY! ===

Additionally, the full end-to-end dashboard test suite (test_dashboard_pages.py) was executed:

Authentic NASA GPM IMERG Mode (2018–2024): 84 months loaded, 7 annual totals computed (
2548.4
 mm
2548.4 mm mean), Mann-Kendall trend test computed (
𝑝
=
0.7639
p=0.7639, Sen's slope 
=
−
11.79
 mm/yr
=−11.79 mm/yr), all Plotly figures generated.
Prototype Multi-Decadal Demo Mode (2000–2024): 300 months loaded, 25 annual totals computed, all figures generated.
Spatial Grid: 320 terrestrial pixels loaded and plotted over Kerala boundary.
Result: [ALL TESTS PASSED] Complete system verified with 0 errors!
5. Summary of Files Changed
File Changed	Summary of Changes
src/statistics.py	• Defined EXPECTED_ANNUAL_COLUMNS, EXPECTED_SEASONAL_COLUMNS, EXPECTED_CLIMATOLOGY_COLUMNS.
• Enforced that compute_annual_totals always returns a DataFrame with named columns even when records are empty.
• Added resilient column lookups for weighted and unweighted rainfall.
• Protected against zero-division in baseline anomaly calculation.
src/visualizer.py	• Added safe guards across plot_annual_rainfall, plot_rainfall_anomalies, plot_seasonal_distribution, plot_monthly_climatology_chart, and plot_kerala_spatial_map.
• Returns informative Plotly annotation figures if DataFrames are empty or missing columns instead of raising KeyError.
src/data_loader.py	• Guarded load_nasa_gpm_data() to return a DataFrame with expected column schema if neither CSV exists.
• Added safe numeric type conversion for the 'year' column.
app.py	• Added has_annual verification before accessing annual metrics or rows.
• Replaced crashing calls with informative st.warning notices when complete annual data is absent.
• Handled single-year temporal filters safely in the sidebar.
AetherNova_NASA_SpaceApps_2026_Submission/	• Synchronized all updated source files (statistics.py, visualizer.py, data_loader.py, app.py) to the clean submission directory.
AetherNova_NASA_SpaceApps_2026.zip	• Rebuilt clean 1.77 MB submission ZIP archive with all fixes and no credentials or secrets included.

(No NASA Earthdata credentials, .env files, or secrets were exposed or modified.)

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
    compute_monthly_climatology,Use Control + Shift + m to toggle the tab key moving focus. Alternatively, use esc then tab to move to the next interactive element on the page.

    compute_seasonal_breakdown,
    run_mann_kendall_test,
)
