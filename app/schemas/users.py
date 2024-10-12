from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime


class UserLoginInfoRead(BaseModel):
    service_type: Optional[str] = None
    user_id: Optional[str] = None
    nickname: Optional[str] = None
    name: Optional[str] = None

    profile_image: Optional[str] = None
    thumbnail_image: Optional[str] = None

    email_address: Optional[str] = None
    connected_at: Optional[datetime] = None

    access_token: Optional[str] = None
    token_type: Optional[str] = None
    refresh_token: Optional[str] = None
    expires_in: Optional[float] = None
    scope: Optional[str] = None
    refresh_token_expires_in: Optional[float] = None

    create_at: Optional[datetime] = None
    create_by: Optional[str] = None
    modify_at: Optional[datetime] = None
    modify_by: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)


# 요청 시 사용할 스키마 (사용자 정보 등록, 업데이트 등)
class UserLoginInfoCreate(BaseModel):
    service_type: str       # PK
    user_id: str            # PK
    nickname: Optional[str] = None
    name: Optional[str] = None

    profile_image: Optional[str] = None
    thumbnail_image: Optional[str] = None

    email_address: Optional[str] = None
    connected_at: Optional[datetime] = None

    access_token: Optional[str] = None
    token_type: Optional[str] = None
    refresh_token: Optional[str] = None
    expires_in: Optional[float] = None
    scope: Optional[str] = None
    refresh_token_expires_in: Optional[float] = None

    create_at: Optional[datetime] = None
    create_by: Optional[str] = None
    modify_at: Optional[datetime] = None
    modify_by: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)



class UserInvestAPIInfoRead(BaseModel):
    service_type: Optional[str] = None
    user_id: Optional[str] = None
    account: Optional[str] = None
    
    api_key: Optional[str] = None
    app_secret: Optional[str] = None
    
    access_token: Optional[str] = None
    token_type: Optional[str] = None
    access_token_expires: Optional[datetime] = None
    expires_in: Optional[float] = None
    
    create_at: Optional[datetime] = None
    create_by: Optional[str] = None
    modify_at: Optional[datetime] = None
    modify_by: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)


class UserInvestAPIInfoCreate(BaseModel):
    service_type: str       # PK
    user_id: str            # PK
    account: str            # PK
    
    api_key: Optional[str] = None
    app_secret: Optional[str] = None
    
    access_token: Optional[str] = None
    token_type: Optional[str] = None
    access_token_expires: Optional[datetime] = None
    expires_in: Optional[float] = None
    
    create_at: Optional[datetime] = None
    create_by: Optional[str] = None
    modify_at: Optional[datetime] = None
    modify_by: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)