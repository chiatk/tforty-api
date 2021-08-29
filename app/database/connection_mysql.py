import os
from sqlalchemy.engine.create import create_engine
from sqlalchemy.sql.schema import MetaData
from sqlalchemy.exc import SQLAlchemyError

meta = MetaData()

def connect():
    try:
    
        host        =   os.environ['host']
        database    =   os.environ['database']
        user        =   os.environ['user']
        password    =   os.environ['password']
        port_db     =   os.environ['port_db']

        engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}:{port_db}/{database}")
        connection = engine.connect()
        meta.create_all(connection)

        return connection

    except SQLAlchemyError as error:
        print( { "Error": "mysql", "name": "connect", "message": error.statement, "code": error.code } )
        return False