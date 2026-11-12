# Scientific Methodology: AetherNova

**Project:** AetherNova – Kerala Rainfall Trend Detective  
**Mission Track:** NASA Space Apps Challenge 2026: Be an Earth System Trend Detective  

---

## 1. Primary Dataset & Science Variables

### NASA GPM IMERG Final Run V07 (`GPM_3IMERGM_07`)
* **Level:** Level 3 Monthly Gridded Product ($0.1^\circ \times 0.1^\circ$ resolution, $\approx 10\text{ km} \times 10\text{ km}$)
* **Target Science Variable:** `/Grid/precipitation`
* **Long Name:** `Merged microwave-infrared-gauge precipitation estimate`
* **Native Metadata Units:** `mm/hr` (time-averaged precipitation rate)
* **Missing Value Code:** `-9999.9`
* **Coordinate Grid:** Cell centers at $-179.95^\circ$ to $+179.95^\circ$ (Longitude) and $-89.95^\circ$ to $+89.95^\circ$ (Latitude).
* **Array Indexing:** `(time, lon, lat)` with shape `(1, 3600, 1800)`.

---

## 2. Temporal Integration Formula

The monthly variable `/Grid/precipitation` in `GPM_3IMERGM` represents the mean rain rate over the calendar month in $\text{mm/hr}$. To calculate accumulated monthly rainfall in $\text{mm}$, the hourly rate is multiplied by the exact number of hours in the specific calendar month:

$$\text{Monthly Accumulated Rainfall } R_m\text{ (mm)} = P_{\text{rate}}\text{ (mm/hr)} \times (D_m \times 24)$$

Where:
* $P_{\text{rate}}$ is the mean rain rate in $\text{mm/hr}$.
* $D_m$ is the number of days in month $m$ (accounting dynamically for leap years: February has 29 days in 2020 and 2024; 28 days otherwise).
* Verification: In the June 2024 granule, `time_bnds` extends from `2024-06-01 00:00:00 UTC` to `2024-07-01 00:00:00 UTC`, establishing a duration of exactly **720.0 hours**.

---

## 3. Spatial Point-in-Polygon Masking & Area-Weighting

### A. Terrestrial Masking
Kerala's rectangular bounding box ($74.85^\circ\text{–}77.45^\circ\text{ E}, 8.25^\circ\text{–}12.85^\circ\text{ N}$) contains $27 \times 47 = 1,269$ grid cells, over 65% of which lie in the Arabian Sea or neighboring states.

Using the official `geoBoundaries gbOpen` Kerala polygon and `shapely.geometry.Point(lon, lat)`, each grid cell center is tested:
$$\text{Pixel } k \in \text{Kerala} \iff \text{Polygon}_{\text{Kerala}}.\text{contains}(\text{Point}(\lambda_k, \phi_k))$$

This isolates exactly **320 terrestrial grid points** spanning an aggregate surface area of:
$$320\text{ cells} \times \approx 121.2\text{ km}^2 \approx 38,784\text{ km}^2$$
tracking Kerala's official land area ($38,863\text{ km}^2$).

### B. Cosine Latitude Area Weighting
Because grid-cell surface area diminishes towards the poles as $\cos(\text{latitude})$, the statewide mean rainfall is calculated using cosine-of-latitude weighting:

$$\bar{R}_{\text{weighted}} = \frac{\sum_{k=1}^{N} R_k \cdot \cos(\phi_k)}{\sum_{k=1}^{N} \cos(\phi_k)}$$

Where:
* $R_k$ is the accumulated monthly rainfall of cell $k$.
* $\phi_k$ is the latitude of cell $k$ in radians.
* $N = 320$ valid terrestrial grid cells.

---

## 4. Statistical Trend Detection

### A. Non-Parametric Mann-Kendall Test
Climate precipitation time series rarely satisfy Gaussian normality and frequently contain extreme storm outliers (such as the 2018 deluge). We employ the non-parametric Mann-Kendall trend test via `pymannkendall`:

The Mann-Kendall test statistic $S$ is computed as:
$$S = \sum_{k=1}^{n-1} \sum_{j=k+1}^{n} \text{sign}(x_j - x_k)$$

Where:
$$\text{sign}(x_j - x_k) = \begin{cases} 
+1 & \text{if } (x_j - x_k) > 0 \\
0 & \text{if } (x_j - x_k) = 0 \\
-1 & \text{if } (x_j - x_k) < 0 
\end{cases}$$

The variance $\text{Var}(S)$ is calculated accounting for ties, and the standardized test statistic $Z$ is evaluated against standard normal distribution thresholds at $\alpha = 0.05$ ($95\%$ confidence level).

### B. Sen's Slope Estimator
The rate of trend change is computed using the median of all pairwise slopes:
$$\beta = \text{Median}\left( \frac{x_j - x_k}{j - k} \right) \quad \forall \quad 1 \le k < j \le n$$
Sen's slope is robust to extreme outlier precipitation years.

---

## 5. Anomaly Estimation

Rainfall anomaly percentage is defined relative to the multi-year baseline mean $\bar{R}_{\text{baseline}}$:
$$\text{Anomaly (\%) } = \left( \frac{R_{\text{year}} - \bar{R}_{\text{baseline}}}{\bar{R}_{\text{baseline}}} \right) \times 100\%$$
Green bars denote surplus precipitation; red bars denote seasonal or annual deficits.
