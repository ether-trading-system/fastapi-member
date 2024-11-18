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

    # 기본 요청 데이터 구성
    request_data = {
        "url_div": "simul",  # 모의투자
        "api_key": kis_user_info.api_key,
        "app_secret": kis_user_info.app_secret
    }

    # access_token과 expires_at이 있는 경우에만 추가
    if kis_user_info.access_token:
        request_data["access_token"] = kis_user_info.access_token
    if kis_user_info.access_token_expires:
        request_data["expires_at"] = kis_user_info.access_token_expires

    try:
        # Market Broker API에 요청
        response = requests.post(MARKET_BROKER_API_URL, json=request_data)

        # 응답 처리
        if response.status_code == 200:
            response_data = response.json()
            header = response_data.get("header", {})
            data = response_data.get("data", {})

            # 표준화된 응답을 반환
            return {"header": header, "data": data}

        else:
            # HTTP 상태 코드가 200이 아닌 경우
            logging.error(f"Authentication failed: {response.status_code} - {response.text}")
            return {
                "header": {"res_code": response.status_code},
                "data": {"error_description": "Authentication failed", "error_code": "HTTP_ERROR"}
            }
        
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        # 예기치 못한 에러 발생 시 표준화된 에러 반환
        return {
            "header": {"res_code": 500},
            "data": {"error_description": str(e), "error_code": "UNEXPECTED_ERROR"}
        }
