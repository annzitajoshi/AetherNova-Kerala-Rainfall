# Installation & Execution Guide: AetherNova

**Project:** AetherNova – Kerala Rainfall Trend Detective  
**Tagline:** Decoding Rainfall. Discovering Patterns.  
**NASA Space Apps Challenge 2026**  

---

## 1. System Requirements

* **Operating System:** Windows 10/11, macOS, or Linux
* **Python Runtime:** Python 3.10 to 3.13 (Verified on Python 3.13.7)
* **Hardware:** Any modern standard CPU, minimum 4 GB RAM, 100 MB free disk space

---

## 2. Installation Steps

### Step 1: Open Terminal / PowerShell
Navigate to the project root directory:
```powershell
cd AetherNova
```

### Step 2: Create and Activate Virtual Environment
On Windows:
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

On macOS / Linux:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Step 3: Install Dependencies
```powershell
pip install -r requirements.txt
```

---

## 3. Running the Dashboard Application

With the virtual environment active, run:
```powershell
streamlit run app.py
```

The Streamlit web server will initialize and launch your default browser at:
`http://localhost:8501`

---

## 4. Exploring the Features

1. **Data Source Engine (Sidebar):**
   - **`🛰️ Authentic NASA GPM IMERG (2018–2024)`:** Displays verified satellite observations across 84 continuous months.
   - **`🧪 Prototype Multi-Decadal Demo (2000–2024)`:** Toggles the full 25-year synthetic model demonstrating multi-decadal trend algorithms.
2. **Navigation Tabs:**
   - **🏠 Home (Overview):** Summary metric cards, annual precipitation chart, and scientific investigation pillars.
   - **📈 Long-term Trends:** Mann-Kendall trend test statistics ($p$-value, Sen's slope, $\tau$) and annual anomaly departures.
   - **🌦️ Seasonal Patterns:** Seasonal rainfall breakdown and monthly climatological envelopes.
   - **🗺️ Spatial / District View:** Interactive map of 320 terrestrial satellite pixels over Kerala.
   - **ℹ️ Mission & Methodology:** Dataset provenance, mathematical formulas, and scientific audit summary.
