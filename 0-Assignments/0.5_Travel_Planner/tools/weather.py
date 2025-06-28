import requests

def get_coordinates(city: str):
    url = "https://nominatim.openstreetmap.org/search"
    params = {"q": city, "format": "json"}
    res = requests.get(url, params=params).json()
    if not res:
        return None
    lat = res[0]['lat']
    lon = res[0]['lon']
    return lat, lon

def get_weather_forecast(city: str):
    coords = get_coordinates(city)
    if not coords:
        return f"Could not find location: {city}"
    
    lat, lon = coords
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current_weather": True,
        "daily": "temperature_2m_max,temperature_2m_min,weathercode",
        "timezone": "auto"
    }

    res = requests.get(url, params=params).json()

    current = res.get("current_weather", {})
    daily = res.get("daily", {})

    out = f"Current weather in {city}: {current.get('temperature')}°C, wind {current.get('windspeed')} km/h.\n\nForecast:\n"
    for i in range(len(daily["time"][:3])):
        day = daily["time"][i]
        temp_max = daily["temperature_2m_max"][i]
        temp_min = daily["temperature_2m_min"][i]
        out += f"{day}: {temp_min}°C – {temp_max}°C\n"
    return out
