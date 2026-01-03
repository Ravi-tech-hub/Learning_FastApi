from fastapi import FastAPI
from routers import user,post,auth
from fastapi.middleware.cors import CORSMiddleware
import time
from fastapi import Request

app=FastAPI()
app.include_router(user.router)
app.include_router(post.router)
app.include_router(auth.router) 

app.add_middleware(CORSMiddleware,allow_origins=["http://localhost:3000"],allow_credentials=True,allow_methods=["*"],allow_headers=["*"])

@app.middleware("http")
async def add_process_time_header(request:Request,call_next):
  start_time=time.time()
  response=await call_next(request)
  process_time=time.time()-start_time
  response.headers["X-Process-Time"]=str(process_time)
  return response

@app.middleware("http")
async def log_requests(request:Request,call_next):
  print(f"Request URL: {request.url}")
  response=await call_next(request)
  print(f"Response Status Code: {response.status_code}")
  return response
