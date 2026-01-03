import os
import asyncio
from google.adk.agents import Agent
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types
import warnings
import logging
logging.basicConfig(level=logging.ERROR)
print("Libraries Imported")

# CONFIGiration
os.environ["GOOGLE_API_KEY"]="AIzaSyBW4WcQf0WpxKRLFcTPOuDFaQUHoMRTiqo"
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "False"
print("API KEY SET:")

# Tools
def get_weather(city:str)->dict:
  """
      Retrieves the current weather report for a specified city.
  """
  print(f"---Tool:get_weather called for city:{city}---")
  city_normalized=city.lower().replace(" ","")
  mock_weather_db={
      "newyork": {"status": "success", "report": "The weather in New York is sunny with a temperature of 25°C."},
      "london": {"status": "success", "report": "It's cloudy in London with a temperature of 15°C."},
      "tokyo": {"status": "success", "report": "Tokyo is experiencing light rain and a temperature of 18°C."},

  }
  if city_normalized in mock_weather_db:
    return mock_weather_db[city_normalized]
  else:
     return {"status": "error", "error_message": f"Sorry, I don't have weather information for '{city}'."}
  

print("Tool set")

# Agent
weather_agent=Agent(
    name="weather_agent",
     model="gemini-2.5-flash",
     description="Provides weather information for specific cities.",
     instruction="You are a helpful weather assistant. "
                "When the user asks for the weather in a specific city, "
                "use the 'get_weather' tool to find the information. "
                "If the tool returns an error, inform the user politely. "
                "If the tool is successful, present the weather report clearly.",
     tools=[get_weather], 
  )
print("Agent set")
# session and runner
session_Service=InMemorySessionService()
APP_NAME="Weather_tutorial.app"
USER_ID="user1"
SESSION_id="session_1"


print("session started")
async def init_session(APP_NAME:str,USER_ID:str,SESSION_id:str)->InMemorySessionService:
      session=await session_Service.create_session(
         app_name=APP_NAME,
         user_id=USER_ID,
         session_id=SESSION_id
      )    
      print(f"Session created: App='{APP_NAME}', User='{USER_ID}', Session='{SESSION_id}'")

print("session completd")

runner=Runner(
   agent=weather_agent,
   app_name=APP_NAME,
   session_service=session_Service
)

# interaction
async def ask(query):
   content=types.Content(role="user",parts=[types.Part(text=query)])
   async for event in runner.run_async(
      user_id=USER_ID,
      session_id=SESSION_id,
      new_message=content
   ):
      if event.is_final_response():
         print("Agent",event.content.parts[0].text)


async def main():
   await init_session(APP_NAME,USER_ID,SESSION_id)
   await ask("What is weather in london")
   await ask("Weather in Paris?")
   await ask("Tell me the weather in New York")

asyncio.run(main())