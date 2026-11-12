# Data Sources & References: AetherNova

**Project:** AetherNova – Kerala Rainfall Trend Detective  
**Challenge:** NASA Space Apps Challenge 2026: Be an Earth System Trend Detective  

---

## 1. Primary Earth Science Datasets

### A. NASA GPM IMERG Final Precipitation L3 1 Month 0.1° x 0.1° V07
* **Short Name:** `GPM_3IMERGM` (Version 07)
* **DOI:** [10.5067/GPM/IMERG/3B-MONTH/07](https://doi.org/10.5067/GPM/IMERG/3B-MONTH/07)
* **Data Provider:** NASA Goddard Earth Sciences Data and Information Services Center (GES DISC) / NASA Earthdata Cloud
* **Cloud OPeNDAP Endpoint:** `https://opendap.earthdata.nasa.gov/collections/C2723754851-GES_DISC/granules/`
* **Dataset Period:** June 2000 – Present
* **Reference Citation:**  
  *Huffman, G. J., Bolvin, D. T., Braithwaite, D., Hsu, K. L., Joyce, R. J., Kidd, C., Nelkin, E. J., Sorooshian, S., Stocker, E. F., Tan, J., & Xie, P. (2020). Integrated Multi-satellitE Retrievals for GPM (IMERG) Version 06. In Satellite Precipitation Measurement (pp. 343-353). Springer, Cham.*

---

## 2. Geospatial Boundary Datasets

### A. geoBoundaries Global Administrative Database (ADM1 - India)
* **Dataset:** geoBoundaries gbOpen (Level ADM1 - Kerala)
* **Data Provider:** William & Mary GeoLab (wmgeolab.org)
* **License:** Creative Commons Attribution 2.5 India (CC BY 2.5 IN)
* **Originating Source:** DataMeet Community & Election Commission of India
* **Coordinate Reference System:** EPSG:4326 (WGS84)
* **Reference Citation:**  
  *Runfola, D., Anderson, A., Baier, H., Cauley, M., Crittenden, D., Diloreto, E., Fagan, M., Grover, J., Hanczyc, E., Hochlov, K., Hopkins, A., Jacobs, C., Kearns, E., Leu, A., Maves, M., Moellering, L., Nesterova, T., Oberman, J., Posner, E., & Sharma, M. (2020). geoBoundaries: A global database of political administrative boundaries. PLoS ONE 15(4): e0231866.*

---

## 3. Meteorological Ground Benchmark References

### A. India Meteorological Department (IMD)
* **Reference Entity:** National Weather Forecasting Centre, India Meteorological Department, Ministry of Earth Sciences, Government of India.
* **Subdivision:** Kerala & Mahe Meteorological Subdivision.
* **Benchmarking Bulletin:** *Monthly Rainfall Summary for June 2024* (Published July 2024).
* **Reference Value:** $489.3\text{ mm}$ (observed ground-station network mean).
* **Usage Context:** Documented as an independent surface rain-gauge reference; used in AetherNova's June 2024 validation audit.

---

## 4. Software & Algorithmic Citations

* **pyMannKendall:**  
  *Hussain, M. M., & Mahmud, I. (2019). pyMannKendall: a python package for non parametric Mann Kendall family of trend tests. Journal of Open Source Software, 4(39), 1556.*
* **SciPy:**  
  *Virtanen, P., Gommers, R., Oliphant, T. E., et al. (2020). SciPy 1.0: fundamental algorithms for scientific computing in Python. Nature Methods, 17(3), 261-272.*
* **Streamlit:**  
  *Streamlit Framework (v1.66+), Snowflake Inc. (https://streamlit.io).*
* **Plotly:**  
  *Plotly Open Source Graphing Library for Python (v7.1+), Plotly Technologies Inc.*
* **Shapely:**  
  *Gillies, S., et al. (2020). Shapely: manipulation and analysis of geometric objects.*
