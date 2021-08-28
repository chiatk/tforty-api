from typing import Optional
from pydantic import BaseModel

class Perk(BaseModel):
    id: Optional[int]
    campaing_id: int
    active : bool
    title: str
    image_url: str
    price: int
    included_items: str
    description: str
    quantity_available: int
