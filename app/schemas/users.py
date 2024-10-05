from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import date


class UserLoginInfoRead(BaseModel):
    service_type: Optional[str] = None
    user_id: Optional[str] = None
    nickname: Optional[str] = None
    name: Optional[str] = None

    profile_image: Optional[str] = None
    thumbnail_image: Optional[str] = None

    email_address: Optional[str] = None
    connected_at: Optional[date] = None

    access_token: Optional[str] = None
    token_type: Optional[str] = None
    refresh_token: Optional[str] = None
    expires_in: Optional[float] = None
    scope: Optional[str] = None
    refresh_token_expires_in: Optional[float] = None

    create_date: Optional[date] = None
    create_by: Optional[str] = None
    modify_date: Optional[date] = None
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
    connected_at: Optional[date] = None

    access_token: Optional[str] = None
    token_type: Optional[str] = None
    refresh_token: Optional[str] = None
    expires_in: Optional[float] = None
    scope: Optional[str] = None
    refresh_token_expires_in: Optional[float] = None

    create_date: Optional[date] = None
    create_by: Optional[str] = None
    modify_date: Optional[date] = None
    modify_by: Optional[str] = None
    
    
    model_config = ConfigDict(from_attributes=True)

