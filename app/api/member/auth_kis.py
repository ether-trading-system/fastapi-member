from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import select
import requests
import logging

from app.schemas.users import UserInvestAPIInfoRead, UserInvestAPIInfoCreate
from app.models.users import UserInvestAPIInfo
from common.utils.postgresql_helper import get_db

router = APIRouter()

REAL_INV_URL = "https://openapi.koreainvestment.com:9443"
DEMO_INV_URL = "https://openapivts.koreainvestment.com:29443"



# 한투 - 신규 API Key 등록
@router.post("/regist-api-info")
async def regist_kis_api(kis_user_info: UserInvestAPIInfoCreate, db: Session = Depends(get_db)):
        logging.info("POST /regist-user start")

        # 기존 유저 정보가 있는지 확인
        result = await db.execute(select(UserInvestAPIInfo).filter(
            UserInvestAPIInfo.service_type == kis_user_info.service_type,
            UserInvestAPIInfo.user_id == kis_user_info.user_id,
            UserInvestAPIInfo.account == kis_user_info.account
        ))
        db_user = result.scalars().first()

        if db_user:
            raise HTTPException(status_code=400, detail="유저 정보가 존재합니다.")

        # 신규 유저 등록
        new_user = UserInvestAPIInfo(
            service_type = kis_user_info.service_type,
            user_id = kis_user_info.user_id,
            account = kis_user_info.account,
            
            api_key = kis_user_info.api_key,
            app_secret = kis_user_info.app_secret,
            
            create_at = datetime.now(),
            create_by = "FastAPI User",
            modify_at = datetime.now(),
            modify_by = "FastAPI User"
        )

        try:
            db.add(new_user)
            await db.commit()
            await db.refresh(new_user)

            logging.info("신규 사용자 등록 완료")
            return new_user

        except Exception as e:
            logging.error(f"사용자 등록 중 오류 발생: {str(e)}")
            await db.rollback()
            raise HTTPException(status_code=500, detail="사용자 등록 중 오류가 발생했습니다.")


# 환경변수로 빼기
MARKET_BROKER_API_URL = "http://localhost:8000/member/get-token"

# 한투 - access token 발급(간편인증)
@router.post("/access-token")
async def get_access_token(kis_user_info: UserInvestAPIInfoRead):
    logging.info("POST /access-token start")

    access_token = kis_user_info.access_token           # F/E Cookie로부터 전달받은 access token
    expires_at = kis_user_info.access_token_expires     # 토큰만료일자

    try:
        # access_token과 expires_at이 없는 경우 (신규 발급 요청)
        if not access_token or not expires_at:
            logging.info("토큰이 없습니다. 신규 발급을 요청합니다.")
            response = requests.post(MARKET_BROKER_API_URL, json={
                "url_div": "simul",  # 모의투자
                "api_key": kis_user_info.api_key,
                "app_secret": kis_user_info.app_secret
            })
        # access_token이 만료된 경우 (갱신 요청)
        elif datetime.fromisoformat(expires_at) < datetime.now():
            logging.info("토큰이 만료되었습니다. 신규 발급을 요청합니다.")
            response = requests.post(MARKET_BROKER_API_URL, json={
                "url_div": "simul",
                "api_key": kis_user_info.api_key,
                "app_secret": kis_user_info.app_secret
            })
        # 유효한 access_token이 존재하는 경우
        else:
            logging.info("유효한 토큰이 이미 존재합니다.")
            return {
                "access_token": access_token,
                "expires_at": expires_at
            }
        
        print(response.json())
        if response.status_code == 200:
            return response.json()
        else:
            logging.error(f"Authentication failed: {response.status_code} - {response.text}")
            raise HTTPException(status_code=response.status_code, detail="Authentication failed")
        
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")