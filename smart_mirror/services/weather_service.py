"""
Weather service using Open-Meteo (no API key).
- Geocoding: https://geocoding-api.open-meteo.com/v1/search
- Forecast:  https://api.open-meteo.com/v1/forecast
Returns a normalized dict:
{
  "temp": 23,                        # °C (int)
  "desc": "Parțial noros",           # ro description
  "wind_kmh": 8,                     # km/h (int)
  "humidity": 50,                    # %
  "location": "Alba Iulia",          # name as returned
}
"""
from __future__ import annotations
import time
import requests
from typing import Optional, Dict, Any

_GEOCODE_URL = "https://geocoding-api.open-meteo.com/v1/search"
_FORECAST_URL = "https://api.open-meteo.com/v1/forecast"
_CACHE: Dict[str, tuple[float, dict]] = {}  # key -> (ts, data)
_TTL = 10 * 60  # 10 minutes

# Common weather codes mapped to RO descriptions (subset; Open-Meteo WMO codes)
_WMO_RO = {
    0:  "Senin",
    1:  "În mare parte senin",
    2:  "Parțial noros",
    3:  "Înnorat",
    45: "Ceață",
    48: "Ceață cu chiciură",
    51: "Burniță ușoară",
    53: "Burniță moderată",
    55: "Burniță puternică",
    61: "Ploaie ușoară",
    63: "Ploaie moderată",
    65: "Ploaie puternică",
    66: "Ploaie înghețată ușoară",
    67: "Ploaie înghețată puternică",
    71: "Ninsoare ușoară",
    73: "Ninsoare moderată",
    75: "Ninsoare puternică",
    77: "Ninsoare granulată",
    80: "Averse ușoare",
    81: "Averse moderate",
    82: "Averse puternice",
    85: "Averse de ninsoare ușoare",
    86: "Averse de ninsoare puternice",
    95: "Furtună",
    96: "Furtună cu grindină ușoară",
    99: "Furtună cu grindină puternică",
}

def _geocode(city: str, country: Optional[str] = None) -> Optional[dict]:
    params = {"name": city, "count": 1, "language": "ro", "format": "json"}
    if country and len(country) == 2:
        params["country_code"] = country.upper()
    r = requests.get(_GEOCODE_URL, params=params, timeout=8)
    r.raise_for_status()
    data = r.json()
    results = data.get("results") or []
    return results[0] if results else None

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

def _normalize(location_name: str, forecast: dict) -> dict:
    cur = forecast.get("current", {})
    temp = cur.get("temperature_2m")
    hum = cur.get("relative_humidity_2m")
    wcode = cur.get("weather_code")
    wind = cur.get("wind_speed_10m")

    desc = _WMO_RO.get(int(wcode) if wcode is not None else -1, "—")
    def _ival(x):
        try: return int(round(float(x)))
        except: return None
    return {
        "temp": _ival(temp),
        "desc": desc,
        "wind_kmh": _ival(wind),
        "humidity": _ival(hum),
        "location": location_name,
    }

def get_current_weather(city: str = "Alba Iulia", country: str = "RO") -> dict:
    """Fetch current weather with simple 10min cache per (city,country)."""
    key = f"{city.strip().lower()},{(country or '').strip().lower()}"
    now = time.time()
    hit = _CACHE.get(key)
    if hit and (now - hit[0]) < _TTL:
        return hit[1]

    geo = _geocode(city, country)
    if not geo:
        # Fallback empty
        data = {"temp": None, "desc": "Indisponibil", "wind_kmh": None, "humidity": None, "location": city}
        _CACHE[key] = (now, data)
        return data

    lat, lon = geo["latitude"], geo["longitude"]
    forecast = _fetch_forecast(lat, lon)
    data = _normalize(geo.get("name", city), forecast)
    _CACHE[key] = (now, data)
    return data

if __name__ == "__main__":
    print(get_current_weather("Alba Iulia", "RO"))

