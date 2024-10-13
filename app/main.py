from fastapi import FastAPI
from app.api.member import auth_kis, auth_kakao, user
from fastapi.middleware.cors import CORSMiddleware

from common.utils.postgresql_helper import engine

# from common.utils.postgresql_helper import engine, Base
from contextlib import asynccontextmanager
from app.models.base import Base
from dotenv import load_dotenv
import os

load_dotenv()

PUBLIC_URL = os.getenv("PUBLIC_URL")
print(PUBLIC_URL)


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        print("create all orm instance")
    yield


app = FastAPI(lifespan=lifespan)

# CORS 설정 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # 필요한 도메인을 추가합니다.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 추가
app.include_router(auth_kis.router, prefix=f"{PUBLIC_URL}/auth-kis", tags=["auth_KIS"])
app.include_router(
    auth_kakao.router, prefix=f"{PUBLIC_URL}/auth-kakao", tags=["auth_Kakao"]
)
app.include_router(user.router, prefix=f"{PUBLIC_URL}/user", tags=["user"])
