
from typing import Optional
from pydantic import BaseModel

class Campaign(BaseModel):
    id: Optional[int]
    user_id: int
    title: str
    chia_wallet: str
    active: bool
    country_id: int
    short_desc: str
    card_image_url: str
    category_id: int
    duration: int
    video_url: str
    video_overlay_image_url: str
    cover_image_url: str
    story: str
    goal: int
    campaign_type_id: int
    founded: bool