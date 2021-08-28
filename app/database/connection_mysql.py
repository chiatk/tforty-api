from sqlalchemy import create_engine, MetaData
import os

host        =   os.environ['host']
database    =   os.environ['database']
user        =   os.environ['user']
password    =   os.environ['password']
port_db     =   os.environ['port_db']

DATABASE_URL = f"mysql+pymysql://{user}:{password}@{host}:{port_db}/{database}"
engine = create_engine(DATABASE_URL)

meta = MetaData()

conn = engine.connect()