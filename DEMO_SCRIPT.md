# AetherNova: Project Demonstration & Video Script

**Project:** AetherNova – Kerala Rainfall Trend Detective  
**Tagline:** Decoding Rainfall. Discovering Patterns.  
**NASA Space Apps Challenge 2026:** Be an Earth System Trend Detective  
**Presenters:** Annzita Joshi & Ashna Maria Saji  
**Target Video Duration:** 3 Minutes  

---

### [0:00 – 0:30] Introduction & Problem Statement
*(Speaker on camera or voiceover over Kerala monsoon / Western Ghats satellite footage)*

> "Hello! We are Team AetherNova, and welcome to our NASA Space Apps Challenge 2026 project: **AetherNova – Kerala Rainfall Trend Detective**. Our tagline is: *Decoding Rainfall. Discovering Patterns.*
> 
> Situated between the warm waters of the Arabian Sea and the towering Western Ghats, Kerala is India's monsoon gateway. But in recent years, Kerala has experienced devastating climate volatility—from the catastrophic 2018 floods to recurring landslide-triggering downpours like Wayanad in 2024. 
> 
> To answer whether Kerala's rainfall is experiencing structural long-term shifts, we built AetherNova using authentic spaceborne satellite observations from NASA's Global Precipitation Measurement mission."

---

### [0:30 – 1:15] Architecture & Cloud-Native Innovation
*(Screen recording of the AetherNova dashboard and NASA Earthdata Cloud OPeNDAP architecture)*

> "Working with satellite data presents a major challenge: global HDF5 files are large and difficult for citizens and decision-makers to process. 
> 
> AetherNova solves this through a cloud-native pipeline. Connecting directly to **NASA Earthdata Cloud OPeNDAP**, our pipeline extracts regional spatial subsets for Kerala. This slashes the monthly data payload by over **99.9%**—from 18 megabytes down to just 9 kilobytes per month!
> 
> Furthermore, Kerala's narrow geography means raw bounding boxes include over 60% Arabian Sea water. We implemented geometric point-in-polygon clipping using the official geoBoundaries Kerala polygon, strictly isolating **320 terrestrial satellite pixels** and weighting each cell by the cosine of latitude."

---

### [1:15 – 2:05] Live Dashboard Walkthrough
*(Screen recording of navigating through the 5 Streamlit dashboard views)*

> "Let's explore the dashboard:
> 
> On the **Home Overview**, users can seamlessly toggle between **Authentic NASA GPM Observations (2018–2024)** and our **Prototype Multi-Decadal Model (2000–2024)**. Dynamic metric cards highlight mean annual rainfall, monsoon contribution percentages, and peak flood years.
> 
> Under **Long-Term Trends**, we deploy the non-parametric **Mann-Kendall test** and **Sen's Slope Estimator** to detect real climate trajectories resilient to flood outliers, accompanied by annual percentage anomaly departures.
> 
> In **Seasonal Patterns**, we decompose Kerala's precipitation into its four meteorological seasons: Southwest Monsoon, Northeast Monsoon, Summer, and Winter.
> 
> And in **Spatial View**, an interactive satellite map displays the spatial rainfall gradient across all 320 terrestrial pixels for our verified June 2024 NASA granule."

---

### [2:05 – 2:40] Scientific Validation & Honest Comparison
*(Screen recording of the Mission & Methodology tab and validation report)*

> "Scientific integrity is at the heart of AetherNova. In our empirical audit of the June 2024 NASA granule:
> - NASA GPM IMERG recorded **404.0 mm** of terrestrial rainfall over Kerala.
> - The India Meteorological Department's ground network recorded **489.3 mm** for the Kerala & Mahe subdivision.
> 
> Rather than assuming direct equivalence, we documented the scientific reasons for this 17.4% divergence: orographic warm-rain undercatch over the Western Ghats by passive microwave sensors, point-gauge versus 10-kilometer area averaging, and differing territorial boundaries."

---

### [2:40 – 3:00] Conclusion & Future Impact
*(Speaker concluding with AetherNova closing slide)*

> "AetherNova demonstrates how open NASA Earth science data, modern geospatial algorithms, and accessible web engineering can empower communities to decode local climate trends.
> 
> We are Annzita Joshi and Ashna Maria Saji. Thank you for exploring AetherNova with us!"
