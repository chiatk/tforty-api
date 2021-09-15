from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse
from sqlalchemy.sql.expression import and_
from ..database.connection_mysql import connect
from ..models.campaign import campaigns
from ..schemas.campaign import Campaign, CampaignUpdate
import shutil
import os
from datetime import datetime

conn = connect()
campaign = APIRouter()


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
    listCampaigns = conn.execute( campaigns.select().where( campaigns.c.active == True ) ).fetchall()

    print(listCampaigns[2]['created'])
    hoy = datetime.now()
    print(hoy.strftime('%d/%m/%Y'))
    return listCampaigns


@campaign.get('/campaigns/{id}', tags=["campaign"])
def find_one_campaign(id: int):
    camp = conn.execute( campaigns.select().where( and_(campaigns.c.id == id, campaigns.c.active == True) )).first()
    if camp is None:
        return { "message": "campaña no existe" }
    return camp

@campaign.put('/campaigns/{id}', tags=["campaign"])
def update_campaign(campaign: CampaignUpdate, id: int):
    camp = conn.execute( campaigns.select().where( and_(campaigns.c.id == id, campaigns.c.active == True) )).first()
    if camp is None:
        return JSONResponse(status_code=400, content={"status": -1, "message": "la campaña no existe" })

    conn.execute(
        campaigns.update()
        .values(
            user_id=                    camp['user_id']                 if campaign.user_id is None else campaign.user_id,
            title=                      camp['title']                   if campaign.title is None else campaign.title,
            chia_wallet=                camp['chia_wallet']             if campaign.chia_wallet is None else campaign.chia_wallet,
            active=                     camp['active']                  if campaign.active is None else campaign.active,
            country_id=                 camp['country_id']              if campaign.country_id is None else campaign.country_id,
            short_desc=                 camp['short_desc']              if campaign.short_desc is None else campaign.short_desc,
            card_image_url=             camp['card_image_url']          if campaign.card_image_url is None else campaign.card_image_url,
            category=                   camp['category']                if campaign.category is None else campaign.category,
            duration=                   camp['duration']                if campaign.duration is None else campaign.duration,
            video_url=                  camp['video_url']               if campaign.video_url is None else campaign.video_url,
            video_overlay_image_url=    camp['video_overlay_image_url'] if campaign.video_overlay_image_url is None else campaign.video_overlay_image_url,
            cover_image_url=            camp['cover_image_url']         if campaign.cover_image_url is None else campaign.cover_image_url,
            story=                      camp['story']                   if campaign.story is None else campaign.story,
            goal=                       camp['goal']                    if campaign.goal is None else campaign.goal,
            campaign_type_id=           camp['campaign_type_id']        if campaign.campaign_type_id is None else campaign.campaign_type_id,
            founded=                    camp['founded']                 if campaign.founded is None else campaign.founded,
            current_balance=            camp['current_balance']         if campaign.current_balance is None else campaign.current_balance
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