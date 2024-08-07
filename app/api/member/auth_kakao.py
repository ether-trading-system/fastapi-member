from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import RedirectResponse, JSONResponse
from app.schemas.kakaoAuth import TokenRequest, TokenResponse
import requests
import logging


router = APIRouter()

AUTHORIZE_ENDPOINT = "https://kauth.kakao.com/oauth/authorize"
ACCESS_TOKEN_ENDPOINT = "https://kauth.kakao.com/oauth/token"

# 카카오 간편인증 - 인가 코드 받기
@router.get("/authorize")
def getAuthCode(redirect_uri: str = Query(..., alias="redirect_uri"), api_key: str = Query(..., alias="api_key")):
    logging.info("GET /getAuthCode 호출")

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

@router.post("/accessToken")
def getAccessToken(token_request: TokenRequest):
    logging.info("POST /getAccessToken 호출")

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