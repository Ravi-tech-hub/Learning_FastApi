from fastapi import FastAPI
app=FastAPI(title="My First FastApi ",description="This is my first fastapi application", version="1.0.0")
@app.get("/")
def root():
  return{"message":"Hello world"}

@app.get("/health")
def health_check():
  return{"status":"healthy"}