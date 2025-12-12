from fastapi import FastAPI
app=FastAPI()

# get-retive data from server
@app.get("/users")
def get_users():
  return [{"id":1,"name":"Ravi"},{"id":2, "name":"Kavi"},{"id":3,"name":"Tavi"}]

# post-create data in server
@app.post("/users")
def create_user():
  return {"message":"User created Successfully"}

@app.put("users/{user_id}")
def update_user(user_id:int):
  return{"message":f"User with id {user_id} updated Successfully"}

@app.delete("users/{user_id}")
def delete_user(user_id:int):
  return {"message":f"user with id {user_id} deleted successfully"}


@app.get("/users/{user_id}")
def get_user(user_id:int):
  print(user_id)
  return {"id":user_id,"name":"Ravi"}