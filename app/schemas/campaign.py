
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
    category_id: int
    duration: int
    video_url: str
    video_overlay_image_url: Optional[str]
    cover_image_url: str
    story: str
    goal: int
    campaign_type_id: Optional[int]
    founded: Optional[bool]