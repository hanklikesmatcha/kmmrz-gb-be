from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    db_name: str
    db_username: str
    db_password: str
    db_host: str
    stripe_secret_key: str
    
settings = Settings()