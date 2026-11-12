# Project Overview: AetherNova – Kerala Rainfall Trend Detective

**Challenge Track:** NASA Space Apps Challenge 2026 — *Be an Earth System Trend Detective*  
**Application Name:** AetherNova  
**Tagline:** Decoding Rainfall. Discovering Patterns.  

---

## 1. Challenge Context & Background

The NASA Space Apps Challenge track **"Be an Earth System Trend Detective"** calls on global participants to leverage authentic NASA Earth observation datasets to detect, visualize, and communicate environmental trends over time.

Kerala, a narrow state on the southwestern tip of India bounded by the Arabian Sea to the west and the Western Ghats mountain range to the east, is a global meteorological hotspot:
* It serves as the primary landfall gateway for the Indian **Southwest Monsoon (Edavappathi)** in early June.
* It receives rainfall from two distinct monsoons: the Southwest Monsoon (June–September) and the Northeast Monsoon (October–November).
* In recent decades, Kerala has witnessed intensifying climate anomalies, including the 2018 Great Deluge, severe localized cloudbursts, and changing inter-seasonal dry-wet cycles.

Understanding whether long-term precipitation is increasing, decreasing, or becoming erratic requires continuous, calibrated Earth observation data.

---

## 2. AetherNova Solution

**AetherNova** bridges the gap between raw NASA satellite files and actionable public climate intelligence.

### Key Capabilities
1. **Cloud-Native Data Ingestion:**
   Connects directly to the **NASA Earthdata Cloud OPeNDAP** service to fetch regional spatial subsets ($74.85^\circ\text{–}77.45^\circ\text{ E}, 8.25^\circ\text{–}12.85^\circ\text{ N}$), shrinking the data payload by 99.95% ($12\text{ KB}$ vs $18.3\text{ MB}$ per month).
2. **Terrestrial Masking Engine:**
   Uses `shapely` point-in-polygon clipping against the official `geoBoundaries` Kerala boundary, ensuring ocean pixels from the Arabian Sea do not distort state-wide terrestrial statistics.
3. **Statistical Trend Detective Suite:**
   Calculates non-parametric **Mann-Kendall test** statistics ($Z$, $\tau$, $p$-value) and **Theil-Sen slope estimates** ($\text{mm/year}$) to discover true multi-year climate trends resilient to outlier storm years.
4. **Interactive Space-Grade Visualization:**
   Displays annual rainfall time-series, historical anomalies (% departure from baseline), 4-season decompositions, monthly climatological envelopes, and interactive geographic scatter maps over a modern dark navy/cyan UI.
5. **Dual Operation Modes:**
   - **Authentic NASA GPM IMERG Mode (2018–2024):** 7 years of fully processed, authentic NASA satellite observations.
   - **Prototype Multi-Decadal Demo Mode (2000–2024):** 25-year synthetic model demonstrating how statistical trend detection behaves over full quarter-century climate normals.

---

## 3. Team & Contributions

* **Annzita Joshi (Team Lead & Full-Stack Developer):**
  - Project management, architecture, and technology selection.
  - NASA Earthdata Cloud OPeNDAP integration and data pipeline engineering.
  - Spatial point-in-polygon geometry and area-weighting algorithms.
  - Statistical trend detection (`pymannkendall` and `scipy`).
  - Full-stack Streamlit frontend development and custom CSS styling.
  - Scientific validation audit against IMD benchmarks.
* **Ashna Maria Saji (NASA Research Contributor):**
  - NASA GPM IMERG V07 product research and GES DISC portal documentation.
  - Identification of variable specifications (`precipitation` in `mm/hr`) and time bounds.
  - Academic literature and ground reference data collection.
  - Presentation content and documentation support.
