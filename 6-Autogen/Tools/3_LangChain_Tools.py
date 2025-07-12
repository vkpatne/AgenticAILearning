import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
import os
import dotenv
dotenv.load_dotenv()

from langchain_community.utilities import GoogleSerperAPIWrapper

from autogen_ext.tools.http import HttpTool


GOOGLE_API_KEY=os.getenv("GOOGLE_API_KEY")

model_client=OpenAIChatCompletionClient(model="gemini-1.5-flash-8b",api_key=GOOGLE_API_KEY)


search_tool_wrapper = GoogleSerperAPIWrapper(type='search')

def search_web(query:str) ->str:
    """Search the web for the given query and return the results."""
    try:
        results = search_tool_wrapper.run(query)
        return results
    except Exception as e:
        print(f"Error occurred while searching the web: {e}")
        return "No results found."  
    

search_agent = AssistantAgent(
    name="SearchAgent",
    model_client=model_client,
    tools=[search_web],
    description="An agent that can search the web for information.",
    system_message="You are a helpful assistant that can search the web for information using the search_web tool." \
    "Please make sure that you use the search_web tool to find information before you return the answer." \
    "don't send the year in query, rather use latest or recently etc.",
    reflect_on_tool_use=True,
)


async def run_serper_search():
    """Run the search agent with a sample query."""
    query = "Who won the IPL recently ?" 
    print(f"Querying: {query}")
    
    
    result = await search_agent.run(task=query)
    print(result.messages[-1].content)


if __name__ == "__main__":
    asyncio.run(run_serper_search())


'''
OUTPUT:

Querying: Who won the IPL recently ?
Royal Challengers Bangalore won the recently concluded IPL 2025.
'''