from typing     import List, Optional
from pydantic   import BaseModel


class User(BaseModel):
    id: Optional[int] = None
    name: Optional[str]
    email: str
    hash_pw: str
    chia_wallet: str
    balance: int
    active: bool

class ResListUser(BaseModel):
    status: bool
    data: List[User]
    
class ResUser(BaseModel):
    status: bool
    data: User

class ErrorUser(BaseModel):
    status: bool= False
    message: str

