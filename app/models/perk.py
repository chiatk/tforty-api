from sqlalchemy import Column, Table
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String, DateTime, Boolean
from sqlalchemy.sql.functions import func
from ..database.connection_mysql import meta, engine

perks = Table(
    "perks",
    meta,
    Column( "id", Integer, primary_key=True ),
    Column( "created", DateTime(timezone=True), server_default=func.now() ),
    Column( "updated", DateTime(timezone=True), onupdate=func.now() ),
    Column( "campaing_id", Integer, ForeignKey("campaigns.id"), nullable=False ),
    Column( "active", Boolean ),
    Column( "title", String(250) ),
    Column( "image_url", String(255) ),
    Column( "price", Integer ),
    Column( "included_items", String(255) ),
    Column( "description", String(255) ),
    Column( "quantity_available", Integer ),
)

meta.create_all(engine)