from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import RedirectResponse, JSONResponse
from app.schemas.kakaoAuth import TokenRequest, TokenResponse
import requests
import logging
import jwt


router = APIRouter()

AUTHORIZE_ENDPOINT = "https://kauth.kakao.com/oauth/authorize"
ACCESS_TOKEN_ENDPOINT = "https://kauth.kakao.com/oauth/token"
USER_INFO_ENDPOINT = "https://kapi.kakao.com/v2/user/me"

# 카카오 간편인증 - 인가 코드 받기
@router.get("/authorize")
def getAuthCode(redirect_uri: str = Query(..., alias="redirect_uri"), api_key: str = Query(..., alias="api_key")):
    logging.info("GET /getAuthCode 요청")

    # 카카오 인증 url로 get 요청
    try:
        ext_url = f"{AUTHORIZE_ENDPOINT}?response_type=code&client_id={api_key}&redirect_uri={redirect_uri}"
        logging.info(f"request url for kakao : {ext_url}")
        response = requests.get(ext_url)

        # API 응답 성공 여부 확인
        response.raise_for_status()

        return RedirectResponse(url=ext_url)
    except requests.RequestException as e:
        logging.error(f"카카오 인증 요청에 실패하였습니다 : {e}")
        raise HTTPException(status_code=500, detail="인증 실패")

# 카카오 간편인증 - Access Token 발급받기
@router.post("/accessToken")
def getAccessToken(token_request: TokenRequest):
    logging.info("POST /getAccessToken 요청")

    try:
        response = requests.post(
            ACCESS_TOKEN_ENDPOINT,
            data=token_request.dict(exclude_none=True)
        )
        response.raise_for_status()

        token_response = response.json()

        return JSONResponse(content=token_response)

    except requests.RequestException as e:
        logging.error(f"Access Token 발급에 실패하였습니다 : {e}")
        raise HTTPException(status_code=500, detail="Access Token 발급 실패")



@router.get("/user_info")
def getUserInfo(access_token: str = Query(..., alias="access_token")):
    logging.info("GET /getUserInfo 호출")

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    try:
        response = requests.get(USER_INFO_ENDPOINT, headers=headers)
        response.raise_for_status()

        user_info = response.json()
        return JSONResponse(content=user_info)

    except requests.RequestException as e:
        logging.error(f"사용자 정보 조회에 실패하였습니다 : {e}")
        raise HTTPException(status_code=500, detail="사용자 정보 조회 실패")


@router.get("/userInfo")
def getUserInfo(access_token: str = Query(..., alias="access_token")):
    logging.info("GET /getUserInfo 요청")

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-type": "application/x-www-form-urlencoded;charset=utf-8"
    }

    try:
        response = requests.get(USER_INFO_ENDPOINT, headers=headers)
        response.raise_for_status()

        user_info = response.json()
        return JSONResponse(content=user_info)
    except requests.RequestException as e:
        logging.error(f"사용자 정보 조회에 실패하였습니다 : {e}")
        raise HTTPException(status_code=500, detail="사용자 정보 조회 실패")


@router.post("/verifyIDToken")
def verifyIDToken(id_token: str):
    try:
        # ID 토큰의 유효성을 검증합니다. 여기서 공개 키를 사용하여 서명을 검증합니다.
        decoded_token = jwt.decode(id_token, options={"verify_signature": False})
        return JSONResponse(content={"decoded_token": decoded_token})
    except jwt.PyJWTError as e:
        logging.error(f"ID 토큰 검증에 실패하였습니다 : {e}")
        raise HTTPException(status_code=400, detail="ID 토큰 검증 실패")