from fastapi import APIRouter
from ..database.connection_mysql import conn
from ..models.campaign import campaigns
from ..schemas.campaign import Campaign

campaign = APIRouter()


@campaign.post('/campaign')
def create_campaign( campaign: Campaign ):
    new_campaign = {
        "user_id": campaign.user_id,
        "title": campaign.title,
        "chia_wallet": campaign.chia_wallet,
        "active": campaign.active,
        "country_id": campaign.country_id,
        "short_desc": campaign.short_desc,
        "card_image_url": campaign.card_image_url,
        "category_id": campaign.category_id,
        "duration": campaign.duration,
        "video_url": campaign.video_url,
        "video_overlay_image_url": campaign.video_overlay_image_url,
        "cover_image_url": campaign.cover_image_url,
        "story": campaign.story,
        "goal": campaign.goal,
        "campaign_type_id": campaign.campaign_type_id,
        "founded": campaign.founded
    }
    result = conn.execute( campaigns.insert().values(new_campaign) )
    return conn.execute( campaigns.select().where( campaigns.c.id == result.lastrowid )).first()

@campaign.get('/campaigns')
def get_campaigns():
    return conn.execute( campaigns.select() ).fetchall()


@campaign.get('/campaigns/{id}')
def find_one_campaign(id: int):
    return conn.execute( campaigns.select().where( campaigns.c.id == id )).first()

@campaign.put('/campaigns/{id}')
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

@campaign.delete('/campaigns/{id}')
def logical_deletion_campaign(id: int):
    conn.execute(
        campaigns.update()
        .values(
            active= False
        )
        .where( campaigns.c.id == id )
    )
    return { "message": f" Se elimino correctamente campaña {id} " }