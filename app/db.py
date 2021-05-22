"""Database functions"""

import os

from dotenv import load_dotenv
from fastapi import APIRouter, Depends
import sqlalchemy

DB = SQLAlchemy()

router = APIRouter()

class Artist(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String(20), nullable=False)

    def __repr__(self):
        return '<Artist {}>'.format(self.name)

# async def get_db() -> sqlalchemy.engine.base.Connection:
#     """Get a SQLAlchemy database connection.
    
#     Uses this environment variable if it exists:  
#     DATABASE_URL=dialect://user:password@host/dbname

#     Otherwise uses a SQLite database for initial local development.
#     """
#     load_dotenv()
#     database_url = os.getenv('DATABASE_URL', default='sqlite:///temporary.db')
#     engine = sqlalchemy.create_engine(database_url)
#     connection = engine.connect()
#     try:
#         yield connection
#     finally:
#         connection.close()


# @router.get('/info')
# async def get_url(connection=Depends(get_db)):
#     """Verify we can connect to the database, 
#     and return the database URL in this format:

#     dialect://user:password@host/dbname
    
#     The password will be hidden with ***
#     """
#     url_without_password = repr(connection.engine.url)
#     return {'database_url': url_without_password}
