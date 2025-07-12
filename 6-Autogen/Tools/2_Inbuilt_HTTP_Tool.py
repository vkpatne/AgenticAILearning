import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_ext.tools.http import HttpTool
import os

GOOGLE_API_KEY=os.getenv("GOOGLE_API_KEY")

model_client=OpenAIChatCompletionClient(model="gemini-1.5-flash-8b",api_key=GOOGLE_API_KEY)

'''
This is a api where output will be:
{
  "fact": "Cats with long, lean bodies are more likely to be outgoing, and more protective and vocal than those with a stocky build.",
  "length": 121
}
'''

schema = {
        "type": "object",
        "properties": {
            "fact": {
                "type": "string",
                "description": "A random cat fact"
            },
            "length": {
                "type": "integer",
                "description": "Length of the cat fact"
            }
        },
        "required": ["fact", "length"],
    }

http_tool = HttpTool(
    name='cat_fact_api',
    description='get a cool cat fact',
    scheme='https',
    host='catfact.ninja',
    port=443,
    path='/fact',
    method='GET',
    return_type='json',
    json_schema=schema
)

agent=AssistantAgent(
     name="CatFactsAgent",
    model_client=model_client,
    system_message='You are a helpful assistant that can provide cat facts using the cat_facts_api tool. Give the result with summary',
    tools=[http_tool],
    reflect_on_tool_use=True
)

async def main(): 
    result = await agent.run(task = 'Give me a random cat fact')

    print(result.messages)

if (__name__ == "__main__"):
    asyncio.run(main())


'''
OUTPUT:

ToolCallExecutionEvent has been triggered.

[TextMessage(id='e8b1ba56-5379-4299-bdb0-3f55353a37ee', source='user', 
models_usage=None, metadata={}, created_at=datetime.datetime(2025, 7, 12, 17, 33, 53, 737886, 
tzinfo=datetime.timezone.utc), content='Give me a random cat fact', type='TextMessage'), 
ToolCallRequestEvent(id='d7864db5-af3e-4541-930d-ab3382140349', source='CatFactsAgent', 
models_usage=RequestUsage(prompt_tokens=56, completion_tokens=9), metadata={}, 
created_at=datetime.datetime(2025, 7, 12, 17, 33, 54, 854535, tzinfo=datetime.timezone.utc), 
content=[FunctionCall(id='', arguments='{"length":100,"fact":"random"}', name='cat_fact_api')], 
type='ToolCallRequestEvent'), ToolCallExecutionEvent(id='3e170485-996b-4764-b3ca-f557412a7fca', 
source='CatFactsAgent', models_usage=None, metadata={}, created_at=datetime.datetime(2025, 7, 12, 17, 33, 55, 442694, 
tzinfo=datetime.timezone.utc), 
content=[FunctionExecutionResult(content="{'fact': 'Tigers are excellent swimmers and do not avoid water.', 'length': 53}",
 name='cat_fact_api', call_id='', is_error=False)], type='ToolCallExecutionEvent'), 

TextMessage(id='056bb07e-f00d-44e0-ba6e-9f46c3f34d67', source='CatFactsAgent', 
models_usage=RequestUsage(prompt_tokens=67, completion_tokens=17), metadata={}, 
created_at=datetime.datetime(2025, 7, 12, 17, 33, 56, 113227, tzinfo=datetime.timezone.utc), 
content="Cats, like tigers, are excellent swimmers and aren't afraid of water.\n", type='TextMessage')]
'''