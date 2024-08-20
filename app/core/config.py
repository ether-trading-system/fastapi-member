import os
from datetime import datetime
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel, Field
from dotenv import load_dotenv


# .env 파일 로드
# load_dotenv()

# class DBSettings(BaseSettings):
#     db_url: str = Field(default='localhost', env='DB_URL')
#     db_port: int = Field(default='5432', env='DB_PORT')            # PostgreSQL 기본포트
#     db_api_key: str = Field(env='DB_API_KEY')

#     model_config = SettingsConfigDict(env_file="postgresql.env")
    


# # API 관련 공통속성 정의(api_key, token_type, expire, secret_code 등등...)
# class API_Config(BaseSettings):
#     api_key: str = Field(env='api_key')
    
    
# # 한투 API 관련 속성 정의
# class API_KIS_Config(API_Config):
#     kis_app_secret: str = Field(env='kis_api_key')
    
# class API_Kakao_Config(API_Config):
#     kakao_rest_key: str = Field(env='kakao_rest_key')


env = os.environ.get("ENV", "")

# Application 기본 설정
class BaseConfig(BaseModel):
    app_name: str = Field(default="FastAPI Application", env='APP_NAME')
    debug_mode: bool = Field(default=False, env='DEBUG_MODE')


# 환경별 설정
class Settings(BaseSettings, BaseConfig):
    model_config = SettingsConfigDict(
        env_prefix='COMMON_',
        env_file_encoding='utf-8',
        env_file=('.env', f'.env.{env}'),
        extra='ignore'
    )


# DB접속정보
class DBConfig(BaseSettings):
    url: str = Field(default='localhost', env='URL')
    port: int = Field(default=1433, env='PORT')            # PostgreSQL 기본포트
    api_key: str = Field(default='None', env='API_KEY')

    model_config = SettingsConfigDict(
        env_prefix='DB_',
        enf_file_encoding='utf-8',
        env_file=('.env', f'.env.{env}'),
        extra='ignore'
    )


# 간편인증(OAuth) Base Config
class OAuthAPIConfig(BaseSettings):
    rest_api_key: str = Field(default="None", env="REST_API_KEY")
    access_token: str = Field(default="Bearer", env="ACCESS_TOKEN")
    token_type: str = Field(default="Bearer", env="TOKEN_TYPE")
    token_expired: datetime = Field(default=None, env="TOKEN_EXPIRED")

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


# Kakao API
class KakaoAPI(OAuthAPIConfig):
    additional_setting: str = Field(default="Default", env="KAKAO_SETTING")

# Google API
class GoogleAPI(OAuthAPIConfig):
    project_id: str = Field(default="None", env="GOOGLE_PROJECT_ID")


# 증권사 API Base Config
class SecurityAPIConfig(BaseSettings):
    app_key: str = Field(default="None", env="APP_KEY")
    app_secret: str = Field(default="None", env="APP_SECRET")

# 한국투자증권 API
class KISAPI(SecurityAPIConfig):
    specific_setting: str = Field(default="Specific", env="KIS_SETTING")

load_dotenv()
settings = Settings()
dbConfig = DBConfig()

print(settings.dict())
print(dbConfig.dict())