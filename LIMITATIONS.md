# Scientific Limitations & Known Uncertainties: AetherNova

**Project:** AetherNova – Kerala Rainfall Trend Detective  
**NASA Space Apps Challenge 2026**  

---

## 1. Discrepancy between Satellite Retrievals and Ground Rain Gauges

In our empirical validation audit of the June 2024 NASA GPM IMERG sample against the India Meteorological Department (IMD) observation:
* **NASA GPM IMERG (Terrestrial Mask):** $404.00\text{ mm}$
* **IMD Ground Observation (Kerala & Mahe):** $489.30\text{ mm}$
* **Discrepancy:** $-85.30\text{ mm}$ ($-17.43\%$)

### Scientific Causes
1. **Orographic Undercatch over the Western Ghats:**
   The Western Ghats induce intense orographic condensation. Passive microwave sounders (GMI, SSMIS, ATMS) rely primarily on scattering by ice hydrometeors in the upper troposphere to detect heavy rain. Warm-rain collision-coalescence processes occurring below the freezing level frequently produce severe ground downpours without large ice columns aloft, resulting in satellite underestimation of Ghats rainfall peaks.
2. **Geographical Domain Divergence:**
   IMD's meteorological subdivision includes the Union Territory enclave of Mahe (Puducherry) and averages rain gauge stations across administrative districts. AetherNova strictly clips terrestrial pixels to the state boundary polygon of Kerala.
3. **Point vs. Spatial Areal Sampling:**
   Rain gauges measure point rainfall over a surface area of $< 0.1\text{ m}^2$, whereas GPM IMERG pixels represent an areal average over $\approx 121.2\text{ km}^2$. High-intensity local downpours are smoothed across the 10 km grid box.
4. **Independence of Data Systems:**
   GPM IMERG V07 Final Run is calibrated globally using GPCC monthly rain-gauge data, which relies on a sparse international GTS network. IMERG is **not calibrated against IMD's complete state-wide rain-gauge network**, and the two datasets must be recognized as complementary rather than equivalent.

---

## 2. Spatial Resolution Limitations

* GPM IMERG provides a $0.1^\circ \times 0.1^\circ$ ($\approx 10\text{ km}$) spatial grid.
* Highly localized microclimates—such as the sharp rainfall shadow across the Palakkad Gap or deep mountain valleys—are spatially blended into adjacent grid values.
* For site-specific engineering or localized flash-flood warnings, ground gauge observations or localized radar data (Doppler Weather Radar) must complement satellite observations.

---

## 3. Boundary Cell Approximations

* AetherNova identifies 320 grid cells whose center coordinates $(\lambda, \phi)$ fall strictly within Kerala's terrestrial boundary.
* A fractional polygon-overlap test revealed that 411 cells touch the boundary (including coastal pixels that extend into the Arabian Sea).
* While the difference in spatial mean between cell-center selection ($404.00\text{ mm}$) and fractional-area weighting ($405.86\text{ mm}$) is minimal ($1.86\text{ mm}$ or $< 0.46\%$), coastal edge pixels inevitably contain minor mixtures of land and sea radar backscatter.

---

## 4. Multi-Decadal Sensor Transition

Across the full GPM IMERG record (2000–present):
* The satellite constellation transitioned from the TRMM era (2000–2014, TRMM Microwave Imager) to the GPM Core Observatory era (2014–present, GPM Microwave Imager).
* Although NASA IMERG V07 performs inter-satellite radiometric calibration to minimize inter-sensor bias, subtle calibration steps between eras can impact weak multi-decadal trends. The non-parametric Mann-Kendall test was selected specifically because it is robust against non-normal steps and extreme outlier years.
