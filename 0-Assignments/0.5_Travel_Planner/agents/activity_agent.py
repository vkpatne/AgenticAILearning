from config import Config
from tools.google_maps import get_nearby_attractions,search_restaurants,get_transport_options
from tools.eventbrite import search_eventbrite_events

cfg = Config()
llm = cfg.llm


tools=[get_nearby_attractions,get_transport_options,search_restaurants,search_eventbrite_events]

llm_with_tools=llm.bind_tools(tools)

response1=llm_with_tools.invoke("Find events in kaichi dham")
print(response1)