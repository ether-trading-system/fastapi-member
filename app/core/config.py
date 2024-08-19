from typing import List, Optional, Union
from pydantic_settings import BaseSettings
from pydantic import Field

class DBConfig(BaseSettings):
    url: str = Field(default='localhost', env='db_url')
    port: int = Field(default=5432, env='db_port')
    api_key: str = Field(env='db_api_key')

    class Config:
        env_file = '.env'

print(DBConfig().dict())
    