import os
from dotenv import load_dotenv

env = os.getenv('FLASK_ENV', 'dev')
load_dotenv(f'.env.{env}')

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    if not SQLALCHEMY_DATABASE_URI:
        raise ValueError("DATABASE_URL environment variable is not set")
    SQLALCHEMY_TRACK_MODIFICATIONS = False