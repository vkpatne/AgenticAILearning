import os
import requests
from langchain.tools import tool
from config import Config


EVENTBRITE_TOKEN = os.getenv("EVENTBRITE_API_TOKEN") or "YOUR_EVENTBRITE_TOKEN"

cfg = Config()
EVENTBRITE_KEY=cfg.EVENTBRITE_KEY

@tool
def search_eventbrite_events(keyword: str, location: str = "India", max_results: int = 5) -> str:
    """
    Search for upcoming events from Eventbrite by keyword and location.
    Returns a list of event titles and their start time.
    """
    url = "https://www.eventbriteapi.com/v3/events/search/"
    headers = {
        "Authorization": f"Bearer {EVENTBRITE_TOKEN}"
    }
    params = {
        "q": keyword,
        "location.address": location,
        "expand": "venue",
        "sort_by": "date",
    }

    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        return f"Error: {response.status_code} - {response.text}"

    data = response.json()
    events = data.get("events", [])[:max_results]

    if not events:
        return f"No events found for '{keyword}' in {location}."

    result_lines = []
    for event in events:
        name = event["name"]["text"]
        start = event["start"]["local"]
        url = event["url"]
        result_lines.append(f"- {name} | {start} | [Link]({url})")

    return "\n".join(result_lines)
