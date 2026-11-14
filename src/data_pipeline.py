"""
AetherNova – Kerala Rainfall Trend Detective
NASA Space Apps Challenge 2026: Be an Earth System Trend Detective

Module: src/data_pipeline.py
Description: Robust, cloud-native downloader and processor for NASA GPM IMERG V07 data over Kerala.
Features:
- Earthdata Cloud OPeNDAP spatial subsetting (reduces bandwidth by >99%)
- Secure, masked token handling via environment or Windows User registry
- Exponential backoff retry logic
- Automatic caching to skip already downloaded months
- Point-in-polygon land masking against official Kerala boundary GeoJSON
- Cosine-of-latitude area-weighted spatial aggregation
"""

import calendar
import json
import logging
import math
import os
from pathlib import Path
import time
from typing import Dict, List, Optional, Tuple
import numpy as np
import pandas as pd
import requests
from shapely.geometry import Point, shape
from shapely.prepared import prep

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("AetherNova.DataPipeline")


class NASADataDownloader:
    """Handles authenticated spatial subset downloading from NASA Earthdata Cloud OPeNDAP."""

    # Kerala bounding box grid indices on GPM IMERG 0.1° grid
    # lon: 74.85 to 77.45 -> indices 2548 to 2574 (27 cells)
    # lat: 8.25 to 12.85  -> indices 982 to 1028  (47 cells)
    LON_START, LON_END = 2548, 2574
    LAT_START, LAT_END = 982, 1028

    OPENDAP_COLLECTION_URL = (
        "https://opendap.earthdata.nasa.gov/collections/C2723754851-GES_DISC/granules/"
    )

    def __init__(self, raw_cache_dir: Optional[Path] = None):
        self.raw_cache_dir = raw_cache_dir or Path(__file__).resolve().parent.parent / "data" / "raw" / "subsets"
        self.raw_cache_dir.mkdir(parents=True, exist_ok=True)
        self.session = self._init_authenticated_session()

    def _init_authenticated_session(self) -> requests.Session:
        """Securely reads the Earthdata token without logging or exposing it."""
        token = os.getenv("EARTHDATA_TOKEN")
        if not token:
            try:
                import winreg
                with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Environment") as key:
                    token, _ = winreg.QueryValueEx(key, "EARTHDATA_TOKEN")
            except Exception:
                pass

        if not token or not str(token).strip():
            raise ValueError("EARTHDATA_TOKEN was not found in environment or Windows User registry.")

        class EarthdataSession(requests.Session):
            def rebuild_auth(self, prepared_request, response):
                headers = prepared_request.headers
                if "Authorization" in self.headers:
                    headers["Authorization"] = self.headers["Authorization"]

        session = EarthdataSession()
        session.headers.update({"Authorization": f"Bearer {token.strip()}"})
        return session

    @staticmethod
    def get_granule_id(year: int, month: int) -> str:
        """Constructs the standard NASA GPM IMERG V07 monthly granule ID."""
        month_str = f"{month:02d}"
        return f"GPM_3IMERGM.07%3A3B-MO.MS.MRG.3IMERG.{year}{month_str}01-S000000-E235959.{month_str}.V07B.HDF5"

    def fetch_monthly_subset(
        self, year: int, month: int, max_retries: int = 3, backoff_factor: float = 2.0
    ) -> Tuple[np.ndarray, List[float], List[float]]:
        """
        Fetches the Kerala spatial subset for a given month.
        Checks local disk cache first. If missing, requests via Cloud OPeNDAP with retries.
        Returns:
            (precip_array_2d, longitudes_list, latitudes_list)
        """
        cache_file = self.raw_cache_dir / f"kerala_subset_{year}_{month:02d}.json"

        # Check Cache
        if cache_file.exists():
            with open(cache_file, "r", encoding="utf-8") as f:
                cached = json.load(f)
            return (
                np.array(cached["precipitation_grid"]),
                cached["lons"],
                cached["lats"],
            )

        granule_id = self.get_granule_id(year, month)
        base_url = f"{self.OPENDAP_COLLECTION_URL}{granule_id}.ascii"
        query = (
            f"?%2FGrid%2Fprecipitation[0:0][{self.LON_START}:{self.LON_END}][{self.LAT_START}:{self.LAT_END}],"
            f"%2FGrid%2Flon[{self.LON_START}:{self.LON_END}],"
            f"%2FGrid%2Flat[{self.LAT_START}:{self.LAT_END}]"
        )
        url = base_url + query

        for attempt in range(1, max_retries + 1):
            try:
                logger.info(f"Downloading subset for {year}-{month:02d} (Attempt {attempt}/{max_retries})...")
                r = self.session.get(url, timeout=30)
                
                if r.status_code == 200:
                    lons, lats, precip_arr = self._parse_opendap_ascii(r.text)
                    # Cache locally
                    cache_data = {
                        "year": year,
                        "month": month,
                        "lons": lons,
                        "lats": lats,
                        "precipitation_grid": precip_arr.tolist(),
                    }
                    with open(cache_file, "w", encoding="utf-8") as f:
                        json.dump(cache_data, f)
                    logger.info(f"Cached subset for {year}-{month:02d} ({cache_file.stat().st_size:,} bytes).")
                    return precip_arr, lons, lats
                elif r.status_code == 404:
                    raise FileNotFoundError(f"Granule for {year}-{month:02d} not found on NASA server (HTTP 404).")
                else:
                    logger.warning(f"HTTP {r.status_code} received on attempt {attempt}: {r.text[:200]}")
            except Exception as e:
                logger.warning(f"Error on attempt {attempt} for {year}-{month:02d}: {e}")
                if attempt == max_retries:
                    raise

            # Exponential backoff
            sleep_time = backoff_factor ** attempt
            time.sleep(sleep_time)

        raise RuntimeError(f"Failed to fetch data for {year}-{month:02d} after {max_retries} attempts.")

    @staticmethod
    def _parse_opendap_ascii(ascii_text: str) -> Tuple[List[float], List[float], np.ndarray]:
        """Parses the OPeNDAP ASCII response into coordinate vectors and 2D rain-rate grid."""
        lons = []
        lats = []
        precip_grid = []

        for line in ascii_text.strip().splitlines():
            line = line.strip()
            if line.startswith("/Grid/lon,"):
                lons = [float(x.strip()) for x in line.split(",")[1:]]
            elif line.startswith("/Grid/lat,"):
                lats = [float(x.strip()) for x in line.split(",")[1:]]
            elif line.startswith("/Grid/precipitation.precipitation["):
                parts = [float(x.strip()) for x in line.split(",")[1:]]
                precip_grid.append(parts)

        if not lons or not lats or not precip_grid:
            raise ValueError("Malformed OPeNDAP ASCII response from NASA server.")

        precip_arr = np.array(precip_grid)
        return lons, lats, precip_arr


class KeralaRainfallProcessor:
    """Applies polygon land-masking and calculates spatial meteorological aggregations."""

    def __init__(self, geojson_path: Optional[Path] = None):
        self.geojson_path = (
            geojson_path
            or Path(__file__).resolve().parent.parent / "assets" / "geojson" / "kerala_boundary.geojson"
        )
        if not self.geojson_path.exists():
            raise FileNotFoundError(f"Kerala boundary GeoJSON not found at: {self.geojson_path}")

        with open(self.geojson_path, "r", encoding="utf-8") as f:
            gj = json.load(f)
        self.kerala_geom = shape(gj["features"][0]["geometry"])
        self.kerala_prep = prep(self.kerala_geom)

    @staticmethod
    def get_season(month: int) -> str:
        """Categorizes calendar month into Kerala meteorological seasons."""
        if month in (6, 7, 8, 9):
            return "Southwest Monsoon (Edavappathi)"
        elif month in (10, 11):
            return "Northeast Monsoon (Thulavarsham)"
        elif month in (12, 1, 2):
            return "Winter"
        else:
            return "Summer / Pre-Monsoon"

    def process_month(
        self, year: int, month: int, precip_grid: np.ndarray, lons: List[float], lats: List[float]
    ) -> Dict:
        """
        Masks the grid against Kerala's boundary, computes area-weighted and unweighted metrics.
        Returns a dictionary record for the monthly timeseries.
        """
        _, days_in_month = calendar.monthrange(year, month)
        total_hours = days_in_month * 24

        valid_pixels = []
        fill_val = -9999.9

        for i, lon_val in enumerate(lons):
            for j, lat_val in enumerate(lats):
                pt = Point(lon_val, lat_val)
                if self.kerala_prep.contains(pt):
                    rate = float(precip_grid[i, j])
                    if rate != fill_val and rate >= 0 and not math.isnan(rate):
                        weight = math.cos(math.radians(lat_val))
                        accum_mm = rate * total_hours
                        valid_pixels.append({
                            "rainfall_mm": accum_mm,
                            "rate_mm_hr": rate,
                            "weight": weight,
                        })

        if not valid_pixels:
            raise ValueError(f"No valid pixels found within Kerala for {year}-{month:02d}.")

        df_pixels = pd.DataFrame(valid_pixels)
        weights = df_pixels["weight"].values
        rain_vals = df_pixels["rainfall_mm"].values

        weighted_mean = float(np.sum(rain_vals * weights) / np.sum(weights))
        unweighted_mean = float(np.mean(rain_vals))
        median_val = float(np.median(rain_vals))
        min_val = float(np.min(rain_vals))
        max_val = float(np.max(rain_vals))
        std_val = float(np.std(rain_vals))

        return {
            "year": year,
            "month": month,
            "month_name": calendar.month_abbr[month],
            "season": self.get_season(month),
            "days_in_month": days_in_month,
            "total_hours": total_hours,
            "valid_pixel_count": len(df_pixels),
            "rainfall_mm_weighted": round(weighted_mean, 2),
            "rainfall_mm_unweighted": round(unweighted_mean, 2),
            "median_mm": round(median_val, 2),
            "min_mm": round(min_val, 2),
            "max_mm": round(max_val, 2),
            "std_mm": round(std_val, 2),
        }
