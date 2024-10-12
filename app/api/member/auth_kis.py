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
@router.post("/create-kis-api")
async def create_kis_api(kis_user_info: UserInvestAPIInfoCreate, db: Session = Depends(get_db)):
        logging.info("POST /create-user start")

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



# 한투 - access token 발급(간편인증)
@router.post("/access-token")
async def run_simple_auth(kis_user_info: UserInvestAPIInfoRead, db: Session = Depends(get_db)):
    logging.info("POST /access-token start")
    # user_appkey = ""
    # user_appsecret = ""
    print(f"kis_user_info.api_key : {kis_user_info.api_key}")
    print(f"kis_user_info.app_secret : {kis_user_info.app_secret}")
    try:
        response = requests.post(f"{DEMO_INV_URL}/oauth2/tokenP", json={
            "grant_type": "client_credentials",     # 고정
            "appkey": kis_user_info.api_key,
            "appsecret": kis_user_info.app_secret
        })

        if response.status_code == 200:
            access_token_info = response.json()

            if "error_code" in access_token_info:
                error_code = access_token_info["error_code"]
                if error_code == "EGW00133":
                    raise HTTPException(status_code=429, detail=f"토큰 발급은 1분당 1회만 가능합니다.")
                else:
                    logging.error(f"API Error: {error_code} - {access_token_info.get('error_message', 'No error message')}")
                    raise HTTPException(status_code=400, detail="토큰 발급에 실패하였습니다. API 요청 전문을 확인하세요.")
            
            # error_code 키가 없으면
            else:
                logging.info("KIS 토큰 발급 성공")
                result = await db.execute(select(UserInvestAPIInfo).filter(
                    UserInvestAPIInfo.service_type == kis_user_info.service_type,
                    UserInvestAPIInfo.user_id == kis_user_info.user_id,
                    UserInvestAPIInfo.account == kis_user_info.account
                ))
                db_user = result.scalars().first()
                
                if not db_user:
                    raise HTTPException(status_code=404, detail="유저 정보를 찾을 수 없습니다.")
                
                # 토큰 정보 업데이트
                db_user.access_token = access_token_info.get("access_token")
                db_user.token_type = access_token_info.get("token_type")
                db_user.expires_in = access_token_info.get("expires_in")
                db_user.access_token_expires = datetime.now() + timedelta(seconds=db_user.expires_in)
                
                # modify_at, modify_by 업데이트
                db_user.modify_at = datetime.now()
                db_user.modify_by = "FastAPI User"

                # 변경사항 적용
                await db.commit()
                await db.refresh(db_user)
                
                return db_user
        
        else:
            logging.error(f"Authentication failed: {response.status_code} - {response.text}")
            raise HTTPException(status_code=response.status_code, detail="Authentication failed")
        
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")



# 한투 - access token 발급(API Key, Secret 사용)
# @router.post("/get-access-token", response_model=UserResponse,
#              summary="access token 발급",
#              description="한국투자증권 access token을 발급받습니다.",
#              response_description="신규 유저의 토큰 정보 반환")
# def get_access_token(request: LoginRequest):
#     try:
#         response = requests.post(f"{DEMO_INV_URL}/oauth2/tokenP", json={
#             "grant_type": "client_credentials",
#             "appkey": request.api_key,
#             "appsecret": request.api_secret
#         })
#         if response.status_code == 200:
#             auth_data = response.json()

#             if "error_code" in auth_data:
#                 error_code = auth_data["error_code"]
#                 if error_code == "EGW00133":
#                     raise HTTPException(
#                         status_code=429, 
#                         detail=f"Rate limit exceeded. Try again after 1 minute"
#                     )
#                 else:
#                     logging.error(f"API Error: {error_code} - {auth_data.get('error_message', 'No error message')}")
#                     raise HTTPException(status_code=400, detail="Authentication failed due to API error")
            
#             # error_code 키가 없으면
#             else:
#                 new_member = User(
#                     access_token = auth_data["access_token"],
#                     expired_date = datetime.strptime(auth_data["access_token_token_expired"], "%Y-%m-%d %H:%M:%S").date(),
#                     access_token_type = auth_data["token_type"],
#                     expires_in = auth_data["expires_in"]
#                 )

#             MEMBERS_DB.append(new_member)

#             return new_member
#         else:
#             logging.error(f"Authentication failed: {response.status_code} - {response.text}")
#             raise HTTPException(status_code=response.status_code, detail="Authentication failed")
#     except Exception as e:
#         logging.error(f"An error occurred: {e}")
#         raise HTTPException(status_code=500, detail="Internal Server Error")
