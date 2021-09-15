from sqlalchemy.sql.schema import Table, Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, DateTime
from sqlalchemy.sql.functions import func
from ..database.connection_mysql import meta

donations = Table(
    "donations",
    meta,
    Column( "id", Integer, primary_key=True ),
    Column( "created", DateTime(timezone=True), server_default=func.now() ),
    Column( "updated", DateTime(timezone=True), onupdate=func.now() ),
    Column( "campaing_id", Integer, ForeignKey("campaigns.id"), nullable=False ),
    Column( "user_id", Integer, ForeignKey("users.id"), nullable=False ),
    Column( "perk_id", Integer, ForeignKey("perks.id"), nullable=False ),
    Column( "amount", Integer ),
    Column( "state_id", Integer ),

)