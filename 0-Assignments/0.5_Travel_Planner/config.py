from langchain_community.llms import OpenAI
from langchain_community.chat_models import ChatOpenAI
from langchain_groq import ChatGroq

import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    def __init__(self):
        # self.llm = ChatOpenAI(temperature=0.7, model="gpt-4")
        self.llm = ChatGroq(model="deepseek-r1-distill-llama-70b")
        
        # API keys
        self.google_places_key=os.getenv("google_places_key")
        self.EVENTBRITE_KEY=os.getenv("EVENTBRITE_KEY")
        self.rapid_api_key=os.getenv("rapid_api_key")
        
        # Search limits
        self.max_attractions = 5
        self.max_restaurants = 5
        self.max_activities = 5