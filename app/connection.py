from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from models import Base
from config import settings

# Define URL to connect to database
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

# Create database if it doesn't exist
engine = create_engine(SQLALCHEMY_DATABASE_URL)
if not database_exists(engine.url):
    create_database(engine.url)

## Creates tables if they don't exist
Base.metadata.create_all(engine)