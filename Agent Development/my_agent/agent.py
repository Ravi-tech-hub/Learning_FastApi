from google.adk.agents.llm_agent import Agent

def get_current_time(city:str)->dict:
  return {"status":"Sucess","city":city,"time":"10.30 AM"}

root_agent = Agent(
    model='gemini-2.5-flash',
    name='root_agent',
    description='A helpful assistant for user questions.',
    instruction="You are a helpful assistant that tells the current time in cities. Use the 'get_current_time' tool for this purpose.",
    tools=[get_current_time]
)
