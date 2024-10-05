import requests
import logging

from fastapi import APIRouter, HTTPException, Query, Depends
from fastapi.responses import RedirectResponse, JSONResponse

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from app.dto.auth_kakao import KakaoTokenRequest, KakaoTokenResponse, KakaoLogoutRequest
from common.utils.postgresql_helper import get_db
from app.models.users import UserLoginInfo
from app.schemas.users import UserLoginInfoRead, UserLoginInfoCreate



router = APIRouter()

KAKAO_AUTHORIZE_ENDPOINT = "https://kauth.kakao.com/oauth/authorize"
KAKAO_ACCESS_TOKEN_ENDPOINT = "https://kauth.kakao.com/oauth/token"
KAKAO_USER_INFO_ENDPOINT = "https://kapi.kakao.com/v2/user/me"
KAKAO_LOGOUT_ENDPOINT = "	https://kapi.kakao.com/v1/user/logout"
KAKAO_UNLINK_ENDPOINT = "	https://kapi.kakao.com/v1/user/unlink"


# 카카오 간편인증 - 인가 코드 받기
@router.get("/login")
async def login(redirect_url: str = Query(..., alias="redirect-url"), api_key: str = Query(..., alias="api-key")):
    logging.info("GET /login start")

    # 카카오 인증 url로 get 요청
    try:
        ext_url = f"{KAKAO_AUTHORIZE_ENDPOINT}?response_type=code&client_id={api_key}&redirect_uri={redirect_url}"
        logging.info(f"request url for kakao : {ext_url}")
        response = requests.get(ext_url)

        # API 응답 성공 여부 확인
        response.raise_for_status()

        return RedirectResponse(url=ext_url)
    except requests.RequestException as e:
        logging.error(f"카카오 인증 요청에 실패하였습니다 : {e}")
        raise HTTPException(status_code=500, detail="인증 실패")


# 카카오 간편인증 - Access Token 발급받기
@router.post("/access-token", summary="access token 발급", description="카카오 OAuth2.0 access token을 발급받습니다.", response_description="access token 반환")
async def get_access_token(token_request: KakaoTokenRequest):
    logging.info("POST /get_access_token start")

    try:
        response = requests.post(
            KAKAO_ACCESS_TOKEN_ENDPOINT,
            data=token_request.dict(exclude_none=True)
        )
        response.raise_for_status()

        token_response = KakaoTokenResponse(**response.json())

        logging.info(token_response.dict())
        return JSONResponse(content=token_response.dict())

    except requests.RequestException as e:
        logging.error(f"Access Token 발급에 실패하였습니다 : {e}")
        raise HTTPException(status_code=500, detail="Access Token 발급 실패")


# token 유효성 검증
# @router.post("/verify-id-token", summary="jwt 토큰 인증", description="jwt를 이용하여 토큰 유효성을 검증합니다.", response_description="인증된 토큰 정보")
# def verify_id_token(id_token: str):
#     try:
#         # ID 토큰의 유효성을 검증합니다. 여기서 공개 키를 사용하여 서명을 검증합니다.
#         decoded_token = jwt.decode(id_token, options={"verify_signature": False})
#         return JSONResponse(content={"decoded_token": decoded_token})
#     except jwt.PyJWTError as e:
#         logging.error(f"ID 토큰 검증에 실패하였습니다 : {e}")
#         raise HTTPException(status_code=400, detail="ID 토큰 검증 실패")
    


# 사용자 정보 조회(access_token 요청방식)
@router.get("/get-user-info")
async def get_user_info(access_token: str):
    logging.info("POST /get_user_info start")

    try:
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        response = requests.get(KAKAO_USER_INFO_ENDPOINT, headers=headers)
        response.raise_for_status()
        user_info = response.json()

        return JSONResponse(content=user_info)
    
    except requests.RequestException as e:
        logging.error(f"사용자 정보 조회 실패 : {e}")
        raise HTTPException(status_code=500, detail="사용자 정보 조회 실패")


# access token 인증방식 - 로그아웃
@router.post("/logout-access-token")
async def logout_by_access_token(request: KakaoLogoutRequest):
    logging.info("POST /logout_by_access_token start")
    
    access_token = request.access_token
    target_id = request.target_id
    try:
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        
        data = {
            "target_id_type": "user_id",
            "target_id": target_id
        }
        response = requests.post(KAKAO_LOGOUT_ENDPOINT, headers=headers, data=data)
        response.raise_for_status()
        logout_info = response.json()
        
        return JSONResponse(content=logout_info)
    
    except requests.RequestException as e:
        logging.error(f"로그아웃 실패 : {e}")
        raise HTTPException(status_code=500, detail="로그아웃 실패")



# 사용자 정보 조회(등록된 사용자 id)
@router.get("/get-user-id/{kakao_id}")
async def get_user_info(kakao_id: str, db: AsyncSession = Depends(get_db)):
    logging.info("GET /get_user_info start")
    
    result = await db.execute(select(UserLoginInfo).where(UserLoginInfo.user_id == kakao_id))
    select_user = result.scalar_one_or_none()
    
    if(select_user is None):
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없음")
    
    return UserLoginInfoRead.from_orm((select_user))


# 신규 사용자 생성
@router.post("/create-kakao-user")
async def create_kakao_user(db: AsyncSession = Depends(get_db)):
    logging.info("POST /create_kakao_user start")
    
    new_user = UserLoginInfo(
        service_type='kakao',
        user_id='1234'
    )
    
    try:
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        
        logging.info(f"사용자 등록 완료")
        return { "user": new_user }
    except SQLAlchemyError as e:
        logging.error(f"신규 사용자 등록 실패 : {str(e)}")
        await db.rollback()
        
        raise HTTPException(Status=400, detail="신규 사용자 등록 실패")