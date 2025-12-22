from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base

DATABASE_URL="sqlite:///./app.db"
engine=create_engine(DATABASE_URL,connect_args={"check_same_thread":False})
SessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)
Base=declarative_base()
# check_same_thread for sqlite:- sqlite normally allowed only one thread to access the databse, while FastAPI use multi-threading so this line allow multi-threading

def get_db():
  db=SessionLocal()
  try:
    yield db
  finally:
    db.close()

# get_db -- This function is a dependency,FastAPI will call it automatically when needed
# db=SessionLocal() -- create a new database session
# yield db -- yield sends the session to: your route ,your CRUD functions

# finally: db.close() -- after the request is done, close the session to free up resources




