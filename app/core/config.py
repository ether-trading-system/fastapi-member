from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
# from dotenv import load_dotenv


# .env 파일 로드
# load_dotenv()

class DB_Config(BaseSettings):
    db_url: str = Field(default='localhost', env='DB_URL')
    db_port: int = Field(default='5432', env='DB_PORT')
    db_api_key: str = Field(env='DB_API_KEY')

    model_config = SettingsConfigDict(env_file="postgresql.env")
    


# API 관련 공통속성 정의(api_key, token_type, expire, secret_code 등등...)
class API_Config(BaseSettings):
    api_key: str = Field(env='api_key')
    
    
# 한투 API 관련 속성 정의
class API_KIS_Config(API_Config):
    kis_app_secret: str = Field(env='kis_api_key')
    
class API_Kakao_Config(API_Config):
    kakao_rest_key: str = Field(env='kakao_rest_key')