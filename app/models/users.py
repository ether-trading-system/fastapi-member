from sqlalchemy import Column, String, Numeric, Date
from .base import Base

# 사용자 로그인 접속 정보
class UserLoginInfo(Base):
    __tablename__ = "user_login_info"
    
    service_type = Column(String, primary_key=True, nullable=False)         # OAuth 제공자(kakao, google....)
    user_id = Column(String, primary_key=True, nullable=False)              # ID
    nickname = Column(String, nullable=True)                                # 닉네임
    name = Column(String, nullable=True)                                    # 이름
    
    profile_image = Column(String, nullable=True)                           # 프로필사진
    thumbnail_image = Column(String, nullable=True)                         # 썸네일 사진
    
    email_address = Column(String, nullable=True)                           # 메일주소
    connected_at = Column(Date, nullable=True)                              # 최초 접속일자
    
    access_token = Column(String, nullable=True)                            # Access Token
    token_type = Column(String, nullable=True)                              # Token Type
    refresh_token = Column(String, nullable=True)                           # 리프레시 Token
    expires_in = Column(Numeric, nullable=True)                             # 만료시간(초)
    scope = Column(String, nullable=True)                                   # 사용자 정보 제공 범위(공백 ' '구분자 사용(kakao 기준))
    refresh_token_expires_in = Column(Numeric, nullable=True)               # 리프레시 Token 만료시간(초)
    
    create_at = Column(Date, nullable=True)                                 # 생성일
    create_by = Column(String, nullable=True)                               # 생성자
    modify_at = Column(Date, nullable=True)                                 # 수정일
    modify_by = Column(String, nullable=True)                               # 수정자


# 사용자 증권 접속 정보
class UserInvestAPIInfo(Base):
    __tablename__ = "user_invest_api_info"
    
    service_type = Column(String, primary_key=True, nullable=False)         # API 제공자(한투, 키움, 대신...)
    user_id = Column(String, primary_key=True, nullable=False)              # 로그인 사용자 ID
    account = Column(String, primary_key=True, nullable=False)              # 계좌번호
    
    api_key = Column(String, nullable=True)                                 # API Key
    app_secret = Column(String, nullable=True)                              # App Secret
    
    access_token = Column(String, nullable=True)                            # Access Token
    token_type = Column(String, nullable=True)                              # Token Type
    access_token_expires = Column(Date, nullable=True)                      # 만료일(날짜)
    expires_in = Column(Numeric, nullable=True)                             # 만료시간(초)
    
    create_at = Column(Date, nullable=True)                                 # 생성일
    create_by = Column(String, nullable=True)                               # 생성자
    modify_at = Column(Date, nullable=True)                                 # 수정일
    modify_by = Column(String, nullable=True)                               # 수정자