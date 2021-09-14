from fastapi import APIRouter, File, UploadFile
from sqlalchemy.sql.expression import and_
from ..database.connection_mysql import connect
from ..models.campaign import campaigns
from ..schemas.campaign import Campaign
import shutil
import os

conn = connect()
campaign = APIRouter()

@campaign.post('/example-upload-image', tags=["campaign"])
def upload_image( title: str, uploaded_image: UploadFile = File(...) ):

    with open(f"assets/{uploaded_image.filename}", "wb") as buffer:
        shutil.copyfileobj(uploaded_image.file, buffer)


    pathImage = os.path.join( os.getcwd(), "assets" )
 
    os.rename( f"{pathImage}/{uploaded_image.filename}", f"{pathImage}/{title}.png" )
    image_url = str(f"{os.environ.get('domain')}/media/{title}.png")

    
    new_campaign = {
        "title": title,
        "card_image_url": image_url
    }
    
    return { "status": 1, "data": new_campaign }

@campaign.post('/campaign', tags=["campaign"])
def create_campaign( campaign: Campaign ):
    new_campaign = {
        "user_id": campaign.user_id,
        "title": campaign.title,
        "chia_wallet": campaign.chia_wallet,
        "active": campaign.active,
        "country_id": campaign.country_id,
        "short_desc": campaign.short_desc,
        "card_image_url": campaign.card_image_url,
        "category": campaign.category,
        "duration": campaign.duration,
        "video_url": campaign.video_url,
        "video_overlay_image_url": campaign.video_overlay_image_url,
        "cover_image_url": campaign.cover_image_url,
        "story": campaign.story,
        "goal": campaign.goal,
        "campaign_type_id": campaign.campaign_type_id,
        "founded": campaign.founded,
        "current_balance": campaign.current_balance
    }
    result = conn.execute( campaigns.insert().values(new_campaign) )
    return conn.execute( campaigns.select().where( campaigns.c.id == result.lastrowid )).first()

@campaign.get('/campaigns', tags=["campaign"])
def get_campaigns():
    return conn.execute( campaigns.select().where( campaigns.c.active == True ) ).fetchall()


@campaign.get('/campaigns/{id}', tags=["campaign"])
def find_one_campaign(id: int):
    camp = conn.execute( campaigns.select().where( and_(campaigns.c.id == id, campaigns.c.active == True) )).first()
    if camp is None:
        return { "message": "campaña no existe" }
    return camp

@campaign.put('/campaigns/{id}', tags=["campaign"])
def update_campaign(campaign: Campaign, id: int):
    conn.execute(
        campaigns.update()
        .values(
            user_id= campaign.user_id,
            title= campaign.title,
            chia_wallet= campaign.chia_wallet,
            active= campaign.active,
            country_id= campaign.country_id,
            short_desc= campaign.short_desc,
            card_image_url= campaign.card_image_url,
            category_id= campaign.category_id,
            duration= campaign.duration,
            video_url= campaign.video_url,
            video_overlay_image_url= campaign.video_overlay_image_url,
            cover_image_url= campaign.cover_image_url,
            story= campaign.story,
            goal= campaign.goal,
            campaign_type_id= campaign.campaign_type_id,
            founded= campaign.founded
        )
        .where( campaigns.c.id == id )
    )
    return conn.execute( campaigns.select().where( campaigns.c.id == id ) ).first()

@campaign.delete('/campaigns/{id}', tags=["campaign"])
def logical_deletion_campaign(id: int):
    conn.execute(
        campaigns.update()
        .values(
            active= False
        )
        .where( campaigns.c.id == id )
    )
    return { "message": f" Se elimino correctamente campaña {id} " }