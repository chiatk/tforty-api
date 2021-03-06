
from typing import Optional
from pydantic import BaseModel



class Campaign(BaseModel):
    id: Optional[int] = None
    user_id: int
    title: str
    chia_wallet: Optional[str]
    active: Optional[bool] = True
    country_id: int
    short_desc: Optional[str]
    card_image_url: str
    category: str
    duration: int
    video_url: str
    video_overlay_image_url: Optional[str]
    cover_image_url: str
    story: str
    goal: int
    campaign_type_id: Optional[int]
    founded: Optional[bool]
    current_balance: Optional[int] = 0

class CampaignUpdate(BaseModel):
    id: Optional[int]
    user_id: Optional[int]
    title: Optional[str]
    chia_wallet: Optional[str]
    active: Optional[bool]
    country_id: Optional[int]
    short_desc: Optional[str]
    card_image_url: Optional[str]
    category: Optional[str]
    duration: Optional[int]
    video_url: Optional[str]
    video_overlay_image_url: Optional[str]
    cover_image_url: Optional[str]
    story: Optional[str]
    goal: Optional[int]
    campaign_type_id: Optional[int]
    founded: Optional[bool]
    current_balance: Optional[int]