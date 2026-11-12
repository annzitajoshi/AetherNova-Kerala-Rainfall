# NASA Space Apps Challenge 2026: Project Submission Text

**Project Title:** AetherNova – Kerala Rainfall Trend Detective  
**Tagline:** Decoding Rainfall. Discovering Patterns.  
**Challenge Track:** Be an Earth System Trend Detective  

---

## 1. Short Project Summary (For Submission Form Header - ~50-100 Words)

AetherNova is an interactive climate intelligence web platform that investigates historical precipitation dynamics across Kerala, India, using authentic NASA Earth science data. Powered by the NASA GPM IMERG V07 monthly calibrated product, AetherNova leverages cloud-native OPeNDAP spatial subsetting, geoBoundaries terrestrial land masking (320 pixels), and non-parametric Mann-Kendall trend detection. Featuring a modern dark-navy dashboard, AetherNova provides clear visual storytelling, seasonal breakdowns, and an honest scientific audit comparing spaceborne retrievals with ground-based meteorological benchmarks.

---

## 2. Detailed Project Description (For Space Apps Project Page)

### The Challenge & Problem
The southern Indian state of Kerala is globally recognized as the entry point of the Indian Southwest Monsoon. However, recent years have seen devastating climate volatility: the 2018 Great Deluge, devastating landslide-triggering rainfall in 2019 and 2024, and severe inter-annual shifts between flash flooding and agricultural drought. Local communities, students, and planners need accessible, scientifically grounded tools to analyze whether rainfall patterns are exhibiting long-term structural changes or intensifying seasonal variance.

### How We Solved It
To address this challenge without the computational overhead of processing multi-gigabyte global satellite archives, Team AetherNova developed an end-to-end cloud-native pipeline:
1. **NASA Earthdata Cloud OPeNDAP Ingestion:** We directly query the NASA GES DISC Earthdata Cloud Hyrax server for `GPM_3IMERGM_07` monthly granules, subsetting strictly the Kerala regional bounding box. This slashes the per-month data transfer by over 99.9% (from 18.26 MB down to 9.35 KB).
2. **Terrestrial Land-Boundary Masking:** Because Kerala borders the Arabian Sea, raw bounding boxes contain over 60% open ocean. Using `shapely` and the official `geoBoundaries` ADM1 boundary, we isolate exactly 320 terrestrial satellite pixels ($0.1^\circ \approx 10\text{ km}$ resolution) and apply cosine-of-latitude area weighting.
3. **Trend Detective Analytics:** We deploy non-parametric Mann-Kendall trend tests and Sen's slope estimators to detect genuine climate trajectories resilient to outlier flood events.
4. **Dual Engine Experience:** The dashboard allows seamless switching between **Authentic NASA GPM Observations (2018–2024)** and a **Prototype Multi-Decadal Synthetic Model (2000–2024)**, ensuring full transparency about what data is observational versus synthetic.
5. **Scientific Rigor & Validation:** Rather than claiming superficial agreement with ground networks, we conducted an empirical validation audit for June 2024 (NASA GPM: $404.0\text{ mm}$ vs. IMD: $489.3\text{ mm}$), documenting why spaceborne passive microwave sounders experience orographic undercatch over the steep Western Ghats.

---

## 3. NASA Data & Space Agency Resources Used

* **NASA GPM IMERG Final Precipitation L3 1 Month 0.1° x 0.1° V07 (`GPM_3IMERGM`)**  
  *Goddard Earth Sciences Data and Information Services Center (GES DISC) / NASA Earthdata Cloud.*
* **NASA Earthdata Cloud OPeNDAP & Common Metadata Repository (CMR)**  
  *Programmatic spatial subsetting and granule identification.*
* **geoBoundaries Global Database of Political Administrative Boundaries (ADM1 - India)**  
  *William & Mary GeoLab (wmgeolab.org).*

---

## 4. Hardware & Software Tools Used

* **Language:** Python 3.13
* **Web Framework:** Streamlit
* **Scientific Libraries:** Pandas, NumPy, SciPy, xarray, netCDF4, Shapely, pyMannKendall
* **Visualization:** Plotly, custom CSS
* **Presentation:** python-pptx
* **Data Protocols:** HTTP/REST, OPeNDAP, GeoJSON

---

## 5. Team AetherNova Contributions

* **Annzita Joshi (Team Lead & Full-Stack Developer):**
  System architecture, NASA Earthdata Cloud OPeNDAP pipeline development, spatial point-in-polygon land masking, statistical modeling, Streamlit frontend development, UI/UX design, and empirical validation audit against IMD ground reference data.
* **Ashna Maria Saji (NASA Research Contributor):**
  NASA GPM IMERG V07 product research, verification of variable names, units, and temporal bounds from GES DISC documentation, literature review, and presentation materials.
