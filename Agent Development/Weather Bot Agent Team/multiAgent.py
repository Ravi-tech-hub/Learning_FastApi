import os
import asyncio
from typing import Optional
from google.adk.agents import Agent
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.adk.tools.tool_context import ToolContext
from google.genai import types
os.environ["GOOGLE_API_KEY"] = "AIzaSyBW4WcQf0WpxKRLFcTPOuDFaQUHoMRTiqo"
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "False"

MODEL = "gemini-2.5-flash-lite"

def say_hello(name: Optional[str] = None) -> str:
    return f"Hello, {name}!" if name else "Hello there!"

def say_goodbye() -> str:
    return "Goodbye! Have a great day."

def get_weather_stateful(city: str, tool_context: ToolContext) -> dict:
    unit = tool_context.state.get("unit", "Celsius")
    data = {"london": 15, "newyork": 25}
    key = city.lower().replace(" ", "")
    if key not in data:
        return {"status": "error", "error_message": "City not found"}

    temp_c = data[key]
    if unit == "Fahrenheit":
        temp = temp_c * 9/5 + 32
        unit_symbol = "°F"
    else:
        temp = temp_c
        unit_symbol = "°C"

    report = f"{city.title()} weather: {temp:.0f}{unit_symbol}"
    tool_context.state["last_city"] = city
    return {"status": "success", "report": report}

greeting_agent = Agent(
    name="greeting_agent",
    model=MODEL,
    description="Handles greetings",
    instruction="Greet the user using say_hello",
    tools=[say_hello]
)

farewell_agent = Agent(
    name="farewell_agent",
    model=MODEL,
    description="Handles farewells",
    instruction="Say goodbye using say_goodbye",
    tools=[say_goodbye]
)
root_agent = Agent(
    name="weather_agent_root",
    model=MODEL,
    description="Main agent that delegates greetings/farewells and handles weather",
    instruction="Delegate greetings and farewells. Handle weather using get_weather_stateful.",
    tools=[get_weather_stateful],
    sub_agents=[greeting_agent, farewell_agent],
    output_key="last_response"
)

session_service = InMemorySessionService()

APP = "weather_app"
USER = "user1"
SESSION = "s1"

async def main():
    await session_service.create_session(
        app_name=APP,
        user_id=USER,
        session_id=SESSION,
        state={"unit": "Celsius"}
    )

    runner = Runner(
        agent=root_agent,
        app_name=APP,
        session_service=session_service
    )

    async def ask(q):
        content = types.Content(role="user", parts=[types.Part(text=q)])
        async for event in runner.run_async(user_id=USER,session_id=SESSION,new_message=content):
            if event.is_final_response():
                print("Agent:", event.content.parts[0].text)

    await ask("Hello")
    await ask("What is the weather in London?")
    await ask("Bye")

asyncio.run(main())
