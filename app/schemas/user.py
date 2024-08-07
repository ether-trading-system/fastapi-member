from datetime import date
from pydantic import BaseModel

class UserBase(BaseModel):
    access_token: str
    expired_date: date
    access_token_type: str
    expires_in: int

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    class Config:
        orm_mode = True
