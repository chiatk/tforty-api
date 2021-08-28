from typing     import Optional
from pydantic   import BaseModel

class User(BaseModel):
    id: Optional[int]
    name: Optional[str]
    email: str
    hash_pw: str
    chia_wallet: str
    balance: int
    active: bool