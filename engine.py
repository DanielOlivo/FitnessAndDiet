import os 
from sqlalchemy import create_engine, URL


url_object = URL.create(
    "postgresql",
    username = os.getenv('USERNAME'),
    password = os.getenv('PASSWORD'),
    port = os.getenv('PORT'),
    database = os.getenv('DBNAME')
)
url_object
engine = create_engine(url_object)