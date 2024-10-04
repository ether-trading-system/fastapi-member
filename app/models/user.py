from sqlalchemy import Column, String, Numeric, Date
from models import Base

class UserLoginInfo(Base):
    __tablename__ = "user_login_info"
    
    service_type = Column(String, primary_key=True, nullable=False)
    user_id = Column(String, primary_key=True, nullable=False)
    nickname = Column(String, nullable=True)
    name = Column(String, nullable=True)
    
    profile_image = Column(String, nullable=True)
    thumbnail_image = Column(String, nullable=True)
    
    email_address = Column(String, nullable=True)
    connected_at = Column(Date, nullable=True)
    
    access_token = Column(String, nullable=True)
    token_type = Column(String, nullable=True)
    refresh_token = Column(String, nullable=True)
    expires_in = Column(Numeric, nullable=True)
    scope = Column(String, nullable=True)
    refresh_token_expires_in = Column(Numeric, nullable=True)
    
    create_date = Column(Date, nullable=True)
    create_by = Column(String, nullable=True)
    modify_date = Column(Date, nullable=True)
    modify_by = Column(String, nullable=True)