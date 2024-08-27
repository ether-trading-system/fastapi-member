from sqlalchemy import Column, String, Integer, DateTime
from app.core.db_manager import Base

class AuthTokenInfo(Base):
    __tablename__ = 'T_AUTH_TOKEN_INFO'

    user_id = Column(String, primary_key=True, index=True)
    provide_by = Column(String, primary_key=True, index=True)
    api_key = Column(String, primary_key=True, index=True)
    auth_code = Column(String, index=True)

    access_token = Column(String, index=True)
    token_type = Column(String, index=True)
    expire_date = Column(DateTime)
    expires = Column(Integer)

    mod_dt = Column(DateTime)
    mod_id = Column(String)
    cr_dt = Column(DateTime)
    cr_id = Column(String)