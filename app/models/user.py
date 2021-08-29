from sqlalchemy import Column, Table
from sqlalchemy.sql.sqltypes import Boolean, Integer, String, DateTime
from sqlalchemy.sql.functions import func
from ..database.connection_mysql import meta

users = Table(
    "users",
    meta,
    Column("id", Integer, primary_key=True),
    Column('created', DateTime(timezone=True), server_default=func.now() ),
    Column('updated', DateTime(timezone=True), onupdate=func.now() ),
    Column("active", Boolean),
    Column("name", String(255)),
    Column("email", String(255), unique=True),
    Column("hash_pw", String(255)),
    Column("chia_wallet", String(255)),
    Column("balance", Integer),
)