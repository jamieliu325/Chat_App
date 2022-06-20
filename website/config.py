import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path('.') / '.env'
# take environment variables from .env
load_dotenv(dotenv_path=env_path)

class Config:
    """
    return the value of the environment variable key (see .env doc)
    """
    TESTING = os.getenv('TESTING')
    FLASK_DEBUG = os.getenv('FLASK_DEBUG')
    SECRET_KEY = os.getenv('SECRET_KEY')
    SERVER = os.getenv('SERVER')