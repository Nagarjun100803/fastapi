'''
This file is for handling Databse connections
'''

from sqlalchemy import create_engine #create_engine is responsible for connecting postgre database
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import settings


# URL_FORMART = database_type://username:password@ip/database_name
SQLALCHEMY_DATABSE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_host}/{settings.database_name}'


engine = create_engine(SQLALCHEMY_DATABSE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) 

# """
#     Note : engine is used to establish a connection
#         session is used to talk to the database.
# """
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try :
        yield db
    finally :
        db.close()

