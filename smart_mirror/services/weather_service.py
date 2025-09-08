# Placeholder weather service; replace with real API integration.
# Suggested: Open-Meteo (no key) or OpenWeather (API key).
# Provide a function like get_current_weather(city) -> dict

def get_current_weather(city: str = "Alba Iulia", country: str = "RO") -> dict:
    # TODO: fetch live weather; return structure like:
    # {"temp": 23, "desc": "Parțial noros", "wind_kmh": 8, "humidity": 50, "location": "Alba Iulia"}
    return {
        "temp": 23,
        "desc": "Parțial noros",
        "wind_kmh": 8,
        "humidity": 50,
        "location": f"{city}"
    }
