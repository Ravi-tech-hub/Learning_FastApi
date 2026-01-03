from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
  app_name:str="Learning Production Level File Structure"
  debug:bool=False
  database_url:str="sqlite:///./test.db"

  secert_key:str
  algorthim:str="HS256"
  access_token_expire_minute:int=30

  class config:
    env_file=".env"


@lru_cache()
def get_settings():
  return Settings()
# lru_cache -- this will cache the settings so that they are not recreated on every request

