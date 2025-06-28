# hotel_tools.py

import requests
from config import Config

cfg = Config()
HOTELS_API_KEY = cfg.rapid_api_key

HOST = "hotels-com-provider.p.rapidapi.com"

headers = {
    "X-RapidAPI-Key": HOTELS_API_KEY,
    "X-RapidAPI-Host": HOST
}

def search_hotels(city: str) -> str:
    # Step 1: get location_id
    loc_url = f"https://{HOST}/v1/hotels/locations"
    res = requests.get(loc_url, headers=headers, params={"query": city, "locale": "en_US"}).json()
    if not res:
        return f"City {city} not found."
    location_id = res[0]["id"]

    # Step 2: search hotels
    search_url = f"https://{HOST}/v1/hotels/search"
    params = {
        "location_id": location_id,
        "adults_number": 1,
        "checkin_date": "2025-07-01",
        "checkout_date": "2025-07-03",
        "sort_order": "STAR_RATING_HIGHEST_FIRST",
        "locale": "en_US",
        "currency": "USD"
    }
    results = requests.get(search_url, headers=headers, params=params).json().get("results", [])
    
    output = []
    for hotel in results[:5]:
        name = hotel["name"]
        price = hotel.get("price", {}).get("lead", {}).get("amount", "N/A")
        output.append(f"{name} - Price: ${price}")
    return "\n".join(output) if output else "No hotels found."
