from pydantic import ValidationError
from pydantic_settings import BaseSettings 

class Settings(BaseSettings):
    
    host_ip: str
    host_port: int

    # TODO: Add other settings here
    

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

try:
    settings = Settings()
except ValidationError as e:
    print(e)
    