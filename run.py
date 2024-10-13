import os

import uvicorn
import webbrowser
from threading import Timer
from app.core.config import BaseConfig
from dotenv import load_dotenv

baseConfig = BaseConfig()

def open_browser():
    webbrowser.open_new(f"http://{baseConfig.app_host}:{baseConfig.app_port}/docs")

def load_env_vars():
    # 기존 환경 변수 덮어쓰기
    load_dotenv(override=True)

if __name__ == "__main__":
    load_env_vars()
    Timer(0.5, open_browser).start()
    uvicorn.run("app.main:app", host=baseConfig.app_host, port=baseConfig.app_port, reload=True)