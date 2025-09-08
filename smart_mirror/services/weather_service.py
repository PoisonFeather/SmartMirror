"""
Weather service cu orașe presetate (lat/lon fixe) — fără geocoding.
Schimbi orașul trimițând cheie din PRESET_CITIES către get_current_weather().
"""
from __future__ import annotations
import time
import requests
from typing import Dict, Tuple, Optional

_FORECAST_URL = "https://api.open-meteo.com/v1/forecast"

# Orașe presetate (poți adăuga oricând)
# Numele din cheie va fi și eticheta afișată în UI.
PRESET_CITIES: Dict[str, Tuple[float, float]] = {
    "Alba Iulia":   (46.0730, 23.5800),
    "Cluj-Napoca":  (46.7712, 23.6236),
    "București":    (44.4268, 26.1025),
    "Iași":         (47.1585, 27.6014),
    "Timișoara":    (45.7489, 21.2087),
    "Brașov":       (45.6579, 25.6012),
    "Constanța":    (44.1598, 28.6348),
    "Sibiu":        (45.7930, 24.1210),
    "Oradea":       (47.0722, 21.9217),
}

# WMO -> descrieri RO (subset util)
_WMO_RO = {
    0: "Senin", 1: "În mare parte senin", 2: "Parțial noros", 3: "Înnorat",
    45: "Ceață", 48: "Ceață cu chiciură",
    51: "Burniță ușoară", 53: "Burniță moderată", 55: "Burniță puternică",
    61: "Ploaie ușoară", 63: "Ploaie moderată", 65: "Ploaie puternică",
    66: "Ploaie înghețată ușoară", 67: "Ploaie înghețată puternică",
    71: "Ninsoare ușoară", 73: "Ninsoare moderată", 75: "Ninsoare puternică",
    77: "Ninsoare granulată",
    80: "Averse ușoare", 81: "Averse moderate", 82: "Averse puternice",
    85: "Averse de ninsoare ușoare", 86: "Averse de ninsoare puternice",
    95: "Furtună", 96: "Furtună cu grindină ușoară", 99: "Furtună cu grindină puternică",
}

# Cache simplu per oraș (10 min)
_CACHE: Dict[str, tuple[float, dict]] = {}
_TTL = 10 * 60  # secunde

def _ival(x):
    try:
        return int(round(float(x)))
    except Exception:
        return None

def _fetch_forecast(lat: float, lon: float) -> dict:
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m",
        "timezone": "auto",
    }
    r = requests.get(_FORECAST_URL, params=params, timeout=8)
    r.raise_for_status()
    return r.json()

def get_current_weather(city_key: str = "Alba Iulia") -> dict:
    """
    city_key trebuie să fie o cheie din PRESET_CITIES (ex: 'Alba Iulia').
    Returnează dict: {temp, desc, wind_kmh, humidity, location}
    """
    if city_key not in PRESET_CITIES:
        # fallback sigur: primul oraș din listă
        city_key = list(PRESET_CITIES.keys())[0]

    now = time.time()
    hit = _CACHE.get(city_key)
    if hit and (now - hit[0]) < _TTL:
        return hit[1]

    lat, lon = PRESET_CITIES[city_key]
    data = _fetch_forecast(lat, lon)
    cur = data.get("current", {})

    wcode = cur.get("weather_code")
    out = {
        "temp": _ival(cur.get("temperature_2m")),
        "desc": _WMO_RO.get(int(wcode) if wcode is not None else -1, "—"),
        "wind_kmh": _ival(cur.get("wind_speed_10m")),
        "humidity": _ival(cur.get("relative_humidity_2m")),
        "location": city_key,  # forțăm eticheta exact ca în preset
    }
    _CACHE[city_key] = (now, out)
    return out

if __name__ == "__main__":
    # Test rapid
    print(get_current_weather("Alba Iulia"))
