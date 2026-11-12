# Scientific Validation Audit: NASA GPM IMERG June 2024 Rainfall over Kerala

**Project:** AetherNova – Decoding Rainfall. Discovering Patterns.  
**Challenge:** NASA Space Apps Challenge 2026: Be an Earth System Trend Detective  
**Audit Target:** June 2024 GPM IMERG V07 Monthly Granule (`3B-MO.MS.MRG.3IMERG.20240601-S000000-E235959.06.V07B.HDF5`)  
**Date of Audit:** November 2026  

---

## 1. Executive Summary & Audit Objective

Before executing the multi-decadal processing pipeline across all months (June 2000 to present), this rigorous scientific validation audit evaluates:
1. The mathematical and temporal validity of the NASA GPM IMERG V07 monthly rainfall conversion.
2. The coordinate indexing, grid-cell center alignment, and spatial masking accuracy against Kerala's official boundary.
3. The sensitivity of spatial aggregation to boundary pixel handling (cell center containment vs. fractional polygon overlap).
4. An honest, transparent comparison against official India Meteorological Department (IMD) observational benchmarks, documenting domain and sensor differences without making unsubstantiated claims of calibration or equivalence.

---

## 2. NASA GPM IMERG V07 Metadata & Temporal Interpretation

### A. Product Identification
* **File:** `3B-MO.MS.MRG.3IMERG.20240601-S000000-E235959.06.V07B.HDF5`
* **Format:** NetCDF-4 / HDF5
* **Variable:** `/Grid/precipitation`
* **Long Name:** `Merged microwave-infrared-gauge precipitation estimate`
* **Native Metadata Units:** `mm/hr`
* **Missing Value (`_FillValue`):** `-9999.9`

### B. Temporal Meaning & Time Bounds Verification
According to the NASA GPM IMERG Algorithm Theoretical Basis Document (ATBD) and file-level metadata inspection:
* `time`: 1401235200 seconds since 1980-01-06 00:00:00 UTC $\rightarrow$ **2024-06-01 00:00:00 UTC**
* `time_bnds[0]`: **2024-06-01 00:00:00 UTC**
* `time_bnds[1]`: **2024-07-01 00:00:00 UTC**
* **Integration Duration:** **720.0 hours** ($30\text{ days} \times 24\text{ hours/day}$)

The variable `precipitation` represents the **mean precipitation rate over the calendar month in mm/hr**. Therefore, calculating accumulated monthly precipitation in millimeters requires multiplying the hourly rate by the exact number of hours in the month:
$$\text{Accumulated Monthly Precipitation (mm)} = \text{precipitation (mm/hr)} \times 720.0$$

---

## 3. Spatial Masking, Coordinate Indexing & Grid Verification

### A. Coordinate System & Grid Structure
* Coordinate Reference System: WGS84 (`EPSG:4326`)
* Resolution: $0.1^\circ \times 0.1^\circ$ regular latitude-longitude grid
* `lon`: 3,600 values from $-179.95^\circ$ to $+179.95^\circ$ (Step: $0.1^\circ$)
* `lat`: 1,800 values from $-89.95^\circ$ to $+89.95^\circ$ (Step: $0.1^\circ$)
* **Key Finding:** Coordinates represent **cell centers** (e.g. $75.05^\circ, 75.15^\circ, \dots, 77.35^\circ$).
* **Array Indexing:** The array is indexed as `(time, lon, lat)` with shape `(1, 3600, 1800)`. Slicing along axis 1 corresponds to Longitude and axis 2 corresponds to Latitude.

### B. Kerala Boundary Geometry
* Boundary Source: `geoBoundaries gbOpen` (IND ADM1 - Kerala), derived from official boundary registries (DataMeet / Election Commission of India).
* Geometry: Valid `Polygon`, Area $\approx 3.2053\text{ sq deg}$.
* Bounding Box:
  - Longitude: $74.8677^\circ\text{ E}$ to $77.4123^\circ\text{ E}$
  - Latitude: $8.2925^\circ\text{ N}$ to $12.7956^\circ\text{ N}$

### C. Sensitivity Analysis: Center-Based vs. Fractional-Area Masking

| Masking Methodology | Total Cells | Cosine Area-Weighted Mean | Unweighted Mean | Minimum Cell | Maximum Cell |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Grid Cell Center Containment** | **320** | **404.00 mm** | **404.34 mm** | 121.68 mm | 712.80 mm |
| **Fractional Polygon Overlap** | **411** | **405.86 mm** | **406.82 mm** | 115.42 mm | 712.80 mm |

**Sensitivity Finding:**  
* The difference between strict cell-center masking (320 cells) and fractional polygon-area weighting (411 intersecting boundary cells) is **$1.86\text{ mm}$ ($< 0.46\%$)**.
* At Kerala's mean latitude ($\approx 10.5^\circ\text{ N}$), one $0.1^\circ \times 0.1^\circ$ grid cell covers $\approx 11.06\text{ km} \times 10.96\text{ km} \approx 121.2\text{ km}^2$.  
* $320\text{ cells} \times 121.2\text{ km}^2 \approx 38,784\text{ km}^2$, which closely tracks Kerala's official terrestrial surface area of $38,863\text{ km}^2$.
* Pixel coverage is 100% valid (0 fill-value or missing pixels within the terrestrial mask).

---

## 4. Quantitative Comparison with IMD Ground Benchmark

### A. Ground-Truth Reference
* **Official IMD Source:** India Meteorological Department (IMD) National Weather Forecasting Centre, Monthly Rainfall Summary (June 2024).
* **IMD Meteorological Subdivision:** **Kerala & Mahe**
* **Observed Value (June 2024):** **489.3 mm**
* **IMD Climatological Normal:** ~648.3 mm (Deficit: $-25\%$ to $-35\%$)

### B. Quantitative Discrepancy

$$\text{NASA GPM IMERG (Terrestrial Mask, Weighted Mean)} = 404.00\text{ mm}$$
$$\text{IMD Observed Rainfall (Kerala \& Mahe Subdivision)} = 489.30\text{ mm}$$
$$\text{Absolute Discrepancy} = 404.00 - 489.30 = -85.30\text{ mm}$$
$$\text{Percentage Discrepancy} = \left(\frac{404.00 - 489.30}{489.30}\right) \times 100\% = -17.43\%$$

### C. Retraction of Unsupported Equivalence Claim
> [!WARNING]
> **Correction & Retraction:**  
> A preliminary response casually mentioned a close agreement with an unverified preliminary figure (~408 mm). That statement is **retracted as scientifically unsupported**. The actual difference between NASA GPM IMERG ($404.0\text{ mm}$) and the official final IMD subdivision observation ($489.3\text{ mm}$) is **$-85.30\text{ mm}$ ($-17.43\%$)**. NASA GPM IMERG must **never** be claimed as "calibrated or validated against IMD".

### D. Scientific Reasons for the Discrepancy
1. **Geographical Domain Differences:**
   - IMD’s figure is for the "Kerala & Mahe" meteorological subdivision, which includes the Union Territory enclave of Mahe (Puducherry) and calculates regional rainfall via an uneven network of ground rain gauges interpolated using district area weights.
   - AetherNova's estimate strictly isolates Kerala's sovereign state boundary polygon and computes a continuous spatial area-weighted raster integral.
2. **Measurement Physics & Orographic Undercatch:**
   - Kerala's precipitation is dominated by orographic lifting against the steep Western Ghats. Satellite passive microwave (PMW) sounders often struggle to capture warm-rain collision-coalescence processes that lack deep convective ice cores aloft, leading to satellite underestimation of torrential Ghats rainbands.
3. **Spatial Scale & Point vs. Areal Sampling:**
   - Rain gauges represent point measurements ($< 0.1\text{ m}^2$) often situated in high-rainfall valleys or urban centers, whereas each GPM pixel averages precipitation over $\approx 121\text{ km}^2$.
4. **Independent Calibration:**
   - GPM IMERG V07 Final Run incorporates monthly calibration from the Global Precipitation Climatology Centre (GPCC). GPCC relies on a sparse international subset of GTS synoptic stations, not IMD's complete state-wide automatic weather station (AWS) network.

---

## 5. Methodological Assumptions & Documented Limitations

1. **Cell Center Selection Assumption:** Grid cells whose center falls inside Kerala's boundary are treated as 100% terrestrial. While fractional overlap alters the spatial mean by only $+1.86\text{ mm}$, users must note this geometric approximation for coastal edge pixels.
2. **Spatial Resolution Limitation:** At $0.1^\circ$ ($\approx 10\text{ km}$), fine-scale microclimates (such as the sharp rainfall drop-off across the Palakkad Gap) are smoothed into regional gradient steps.
3. **Satellite Sensor Drift & Transition:** Across 2000–present, IMERG merges varying passive microwave constellations (TMI, GMI, SSMIS, AMSR2). Long-term trend analysis must consider potential inter-sensor calibration nuances, which will be handled via non-parametric Mann-Kendall tests.

---

## 6. Recommendations for Multi-Decadal Pipeline

* **Preserve Area Weighting:** Retain cosine-of-latitude weighting ($w_i = \cos(\text{lat}_i)$) for all historical months.
* **Retain Both Masks:** Save both the 320-cell terrestrial point mask and the district-level assignment tables for modular Phase 2 spatial views.
* **Scientific Transparency:** In the public dashboard, present NASA GPM IMERG as a spaceborne satellite-gauge reanalysis product, explicitly framing IMD station data as a complementary reference rather than a direct 1-to-1 equivalence.
