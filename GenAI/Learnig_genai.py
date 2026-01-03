from google import genai
from google.genai import types
# client are object that send our question to gemini
client=genai.Client(api_key="AIzaSyBW4WcQf0WpxKRLFcTPOuDFaQUHoMRTiqo")
question=[ "What is Python?",
    "Why do people use Python?",
    "Give me a simple example"]

for q in question:
  response=client.models.generate_content(
  model="gemini-2.5-flash-lite",
  contents=q
)
print(response.text)


# Text input and image output
# res=client.models.generate_content(
#   model="gemini-2.5-flash-lite",
#   contents="A cartoon infographic for flying sneakers",
#   config=types.GenerateContentConfig(
#     response_modalities=["IMAGE"],
#   ),
# )

# for part in res.parts:
#   if part.inline_data:
#     image=part.as_image()
#     image.show()
# text to image is not working du


# file = client.files.upload(file="C:\Users\Ravip\fastApi-Learning\GenAI\1.txt")
# res = client.models.generate_content(
#     model="gemini-2.5-flash-lite",
#     contents=["Could you summarize this file?", file]
# )

# print(res.text)



client.close()


# client = genai.Client(
#     api_key="YOUR_API_KEY",
#     http_options=types.HttpOptions(api_version="v1")
# )