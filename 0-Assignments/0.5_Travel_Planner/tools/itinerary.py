# itinerary_tools.py

from typing import Literal

def get_day_plan(input_str: str) -> str:
    """
    Input: 'Paris, Day 1, interests: art, food'
    """
    city, day, *rest = [x.strip() for x in input_str.split(",")]
    interests = rest[0].replace("interests:", "").strip() if rest else "sightseeing"
    
    # Example static response (LLM could be used instead)
    return f"""
Day {day} in {city}:
- 9:00 AM – Visit the Louvre Museum
- 12:00 PM – Lunch at Le Comptoir du Relais
- 2:00 PM – Walk through Montmartre art district
- 5:00 PM – Coffee at Café de Flore
- 7:00 PM – Dinner cruise on the Seine
(Interests: {interests})
"""

def create_itinerary(input_str: str) -> str:
    """
    Input: 'Trip to Rome, 3 days, interests: culture, food'
    """
    # Parse input
    parts = [x.strip() for x in input_str.split(",")]
    city = parts[0].replace("Trip to", "").strip()
    days = int([x for x in parts if "day" in x.lower()][0].split()[0])
    interests = [x for x in parts if "interest" in x.lower()]
    interest_val = interests[0].replace("interests:", "").strip() if interests else "general"

    # Simulated itinerary
    itinerary = []
    for i in range(1, days+1):
        itinerary.append(get_day_plan(f"{city}, Day {i}, interests: {interest_val}"))
    return "\n".join(itinerary)
