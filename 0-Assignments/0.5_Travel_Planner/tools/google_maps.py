from langchain.tools import tool
import googlemaps
from config import Config

cfg = Config()
gmaps = googlemaps.Client(key=cfg.google_places_key)


@tool
def get_nearby_attractions(location: str, radius: int = 3000, type: str = "tourist_attraction") -> list:
    """Find nearby tourist attractions based on a location within a specified radius (in meters)."""
    geocode_result = gmaps.geocode(location)
    if not geocode_result:
        return ["Location not found"]

    latlng = geocode_result[0]["geometry"]["location"]

    places_result = gmaps.places_nearby(
        location=latlng,
        radius=radius,
        type=type
    )

    results = places_result.get("results", [])
    attractions = []
    for place in results[:5]:  # limit to 5 results
        name = place.get("name", "")
        address = place.get("vicinity", "")
        rating = place.get("rating", "N/A")
        attractions.append(f"{name} ({rating}/5) - {address}")
    print("attractions", attractions)
    return attractions


@tool
def get_transport_options(origin: str, destination: str, mode: str = "transit"):
    """
    Get transport options (driving, walking, bicycling, transit) between origin and destination.
    Returns duration and distance for each mode.
    """
    results = []
    directions = gmaps.directions(origin, destination, mode=mode)
    if directions:
        leg = directions[0]["legs"][0]
        duration = leg["duration"]["text"]
        distance = leg["distance"]["text"]
        results.append(f"{mode.capitalize()}: {duration}, {distance}")
    return "\n".join(results)


@tool
def search_restaurants(location: str, keyword: str = "restaurant", radius: int = 2000, max_results: int = 5):
    """
    Search for restaurants near a location.

    Parameters:
    - location (str): name of city or landmark (e.g. "Paris", "Statue of Liberty")
    - keyword (str): optional search term (e.g. "Italian", "vegan", "sushi")
    - radius (int): search radius in meters
    - max_results (int): how many top results to return

    Returns:
    - List of restaurant details
    """
    # Geocode location to get lat/lng
    geocode_result = gmaps.geocode(location)
    if not geocode_result:
        return f"Could not find location: {location}"
    
    latlng = geocode_result[0]['geometry']['location']
    lat, lng = latlng['lat'], latlng['lng']

    # Search nearby restaurants
    results = gmaps.places_nearby(
        location=(lat, lng),
        radius=radius,
        keyword=keyword,
        type="restaurant"
    )

    places = results.get("results", [])
    output = []
    for place in places[:max_results]:
        name = place.get("name")
        address = place.get("vicinity")
        rating = place.get("rating", "N/A")
        output.append(f"{name} - {address} - Rating: {rating}")
    
    return "\n".join(output) if output else "No restaurants found."