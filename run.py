import uvicorn
import webbrowser
from threading import Timer
from app.core.config import BaseConfig

baseConfig = BaseConfig()

def open_browser():
    webbrowser.open_new(f"http://{baseConfig.app_host}:{baseConfig.app_port}/docs")

if __name__ == "__main__":
    Timer(0.5, open_browser).start()
    uvicorn.run("app.main:app", host=baseConfig.app_host, port=baseConfig.app_port, reload=True)