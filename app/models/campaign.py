from re import T
from sqlalchemy import Column, Table, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String, DateTime, Boolean
from sqlalchemy.sql.functions import func
from ..database.connection_mysql import meta, engine

campaigns = Table(
    "campaigns",
    meta,
    Column( "id", Integer, primary_key=True ),
    Column( "created", DateTime(timezone=True), server_default=func.now() ),
    Column( "updated", DateTime(timezone=True), onupdate=func.now() ),
    Column( "user_id", Integer, ForeignKey("users.id"), nullable=False ),
    Column( "active", Boolean ),
    Column( "title", String(250) ),
    Column( "chia_wallet", String(255) ),
    Column( "country_id", Integer ),
    Column( "short_desc", String(250) ),
    Column( "card_image_url", String(250) ),
    Column( "category_id", Integer ),
    Column( "duration", Integer ),
    Column( "video_url", String(250) ),
    Column( "video_overlay_image_url", String(250) ),
    Column( "cover_image_url", String(250) ),
    Column( "story", String(250) ),
    Column( "goal", Integer ),
    Column( "campaign_type_id", Integer ),
    Column( "founded", Boolean ),
)


meta.create_all(engine)