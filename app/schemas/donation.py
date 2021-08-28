from typing import Optional
from pydantic import BaseModel

class Donation(BaseModel):
    id: Optional[int]
    amount: int
    campaing_id: int
    user_id: int
    perk_id: int
    state_id: int
