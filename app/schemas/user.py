from typing     import List, Optional
from pydantic   import BaseModel


class User(BaseModel):
    id: Optional[int] = None
    name: str
    email: str
    hash_pw: str
    chia_wallet: Optional[str]
    balance: Optional[int]
    active: Optional[bool] = True

class UpdateUser(BaseModel):
    name: Optional[str]
    email: Optional[str]
    hash_pw: Optional[str]
    chia_wallet: Optional[str]
    balance: Optional[int]
    active: Optional[bool]

class ResListUser(BaseModel):
    status: bool
    data: List[User]
    
class ResUser(BaseModel):
    status: bool
    data: User

class ErrorUser(BaseModel):
    status: bool= False
    message: str


class LoginUser(BaseModel):
    email: str
    password: str