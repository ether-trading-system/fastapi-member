from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
# from dotenv import load_dotenv


# .env 파일 로드
# load_dotenv()

# Config 설정 또한 Hierarchy 구조로 설정 가능
# ex) class PostgreSQL(DB_Config): .....

# env에 Key Name을 지정하도록 되어져 있는데 key name과 필드값의 명이 다르면 에러가 나네...?? 뭐지?? -_-;;
class DB_Config(BaseSettings):
    db_url: str = Field(default='localhost', env='db_url')
    db_port: int = Field(default='5432', env='db_port')
    db_api_key: str = Field(env='db_api_key')

    model_config = SettingsConfigDict(env_file="postgresql.env")
    


# API 관련 공통속성 정의(api_key, token_type, expire, secret_code 등등...)
class API_Config(BaseSettings):
    api_key: str = Field(env='api_key')
    
    
# 한투 API 관련 속성 정의
class API_KIS_Config(API_Config):
    kis_app_secret: str = Field(env='kis_api_key')
    
class API_Kakao_Config(API_Config):
    kakao_rest_key: str = Field(env='kakao_rest_key')