from sqlalchemy import Column, String, Integer, DateTime
from app.core.db_manager import Base

class AuthTokenInfo(Base):
    __tablename__ = 'T_AUTH_TOKEN_INFO'

    user_id = Column("USER_ID", String, primary_key=True, index=True)
    provide_by = Column("PROVIDE_BY", String, primary_key=True, index=True)
    api_key = Column("API_KEY", String, primary_key=True, index=True)
    auth_code = Column("AUTH_CODE", String, index=True)

    access_token = Column("ACCESS_TOKEN", String, index=True)
    token_type = Column("TOKEN_TYPE", String, index=True)
    expire_date = Column("EXPIRE_DATE", DateTime)
    expires = Column("EXPIRES", Integer)

    mod_dt = Column("MOD_DT", DateTime)
    mod_id = Column("MOD_ID", String)
    cr_dt = Column("CR_DT", DateTime)
    cr_id = Column("CR_ID", String)