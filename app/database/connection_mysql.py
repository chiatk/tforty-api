from sqlalchemy import create_engine, MetaData
import os
import yaml
from typing import Dict


with open(os.getcwd() + "/config.yaml") as f:
            pool_config: Dict = yaml.safe_load(f)

user=pool_config['database_url']['user']
dbpass=pool_config['database_url']['pass']
host=pool_config['database_url']['host']
port=pool_config['database_url']['port']
database=pool_config['database_url']['database']

DATABASE_URL = f"mysql+pymysql://{user}:{dbpass}@{host}:{port}/{database}"
engine = create_engine(DATABASE_URL)

meta = MetaData()

conn = engine.connect()