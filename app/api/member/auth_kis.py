from fastapi import APIRouter, HTTPException, Depends, Query
from fastapi.responses import RedirectResponse
from app.schemas.user import UserCreate, UserResponse
from app.models.user import User
from datetime import datetime, timedelta
from typing import List
from pydantic import BaseModel
import uuid
import requests
import logging

router = APIRouter()

REAL_INV_URL = "https://openapi.koreainvestment.com:9443"
DEMO_INV_URL = "https://openapivts.koreainvestment.com:29443"

# ===========================================================================================
# 일단은 In-Memory storage에 저장... 추후에 DB로 관리
API_KEYS_DB = {
    "kimdaewhi": {
        "appkey": "PS2ZuCSGIUOU4R0M3UYVxaWsDMSYYecvAtYV",
        "appsecret": "DZxy0nVMEmkDEaEg4bVqmpjA4z+eWQ6kZ/z4hs68UGKgSP/GRIQ9xPqW01hQba15Jx7L73snAAdfJ+iiyypXuRDgrppTgWWtVg84BGzxHQFf60E3YxMyX1GTizCzUV4Zsns40rUwaZYVHYOpXuwcWVyL9sEEazNY+caPNc4iE17KfwEtGM4="
    },    
}
MEMBERS_DB: List[User] = []

# ===========================================================================================

class LoginRequest(BaseModel):
    api_key: str
    api_secret: str

class RegisterRequest(BaseModel):
    username: str
    api_key: str
    api_secret: str

class SimpleAuthRequest(BaseModel):
    username: str


# 한투 - 유저 등록
@router.post("/register", status_code=201)
def register(request: RegisterRequest):
    if request.username in API_KEYS_DB:
        raise HTTPException(status_code=400, detail="Username already exists")
    API_KEYS_DB[request.username] = {
        "api_key": request.api_key,
        "api_secret": request.api_secret
    }
    return {"msg": "User registered successfully"}



# 한투 - access token 발급(간편인증)
@router.post("/getAccessTokenByKakao", response_model=UserResponse)
def execSimpleAuth(request: SimpleAuthRequest):
    if request.username not in API_KEYS_DB:
        raise HTTPException(status_code=404, detail="User not found")
    
    user_api_info = API_KEYS_DB[request.username]
    user_appkey = user_api_info["appkey"]
    user_appsecret = user_api_info["appsecret"]

    try:
        response = requests.post(f"{DEMO_INV_URL}/oauth2/tokenP", json={
            "grant_type": "client_credentials",
            "appkey": user_appkey,
            "appsecret": user_appsecret
        })

        if response.status_code == 200:
            auth_data = response.json()

            if "error_code" in auth_data:
                error_code = auth_data["error_code"]
                if error_code == "EGW00133":
                    raise HTTPException(
                        status_code=429, 
                        detail=f"Rate limit exceeded. Try again after 1 minute"
                    )
                else:
                    logging.error(f"API Error: {error_code} - {auth_data.get('error_message', 'No error message')}")
                    raise HTTPException(status_code=400, detail="Authentication failed due to API error")
            
            # error_code 키가 없으면
            else:
                new_member = User(
                    access_token = auth_data["access_token"],
                    expired_date = datetime.strptime(auth_data["access_token_token_expired"], "%Y-%m-%d %H:%M:%S").date(),
                    access_token_type = auth_data["token_type"],
                    expires_in = auth_data["expires_in"]
                )

            MEMBERS_DB.append(new_member)
            return new_member
        
        else:
            logging.error(f"Authentication failed: {response.status_code} - {response.text}")
            raise HTTPException(status_code=response.status_code, detail="Authentication failed")
        
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")



# 한투 - access token 발급(API Key, Secret 사용)
@router.post("/getAccessToken", response_model=UserResponse)
def getAccessToken(request: LoginRequest):
    try:
        response = requests.post(f"{DEMO_INV_URL}/oauth2/tokenP", json={
            "grant_type": "client_credentials",
            "appkey": request.api_key,
            "appsecret": request.api_secret
        })
        if response.status_code == 200:
            auth_data = response.json()

            if "error_code" in auth_data:
                error_code = auth_data["error_code"]
                if error_code == "EGW00133":
                    raise HTTPException(
                        status_code=429, 
                        detail=f"Rate limit exceeded. Try again after 1 minute"
                    )
                else:
                    logging.error(f"API Error: {error_code} - {auth_data.get('error_message', 'No error message')}")
                    raise HTTPException(status_code=400, detail="Authentication failed due to API error")
            
            # error_code 키가 없으면
            else:
                new_member = User(
                    access_token = auth_data["access_token"],
                    expired_date = datetime.strptime(auth_data["access_token_token_expired"], "%Y-%m-%d %H:%M:%S").date(),
                    access_token_type = auth_data["token_type"],
                    expires_in = auth_data["expires_in"]
                )

            MEMBERS_DB.append(new_member)

            return new_member
        else:
            logging.error(f"Authentication failed: {response.status_code} - {response.text}")
            raise HTTPException(status_code=response.status_code, detail="Authentication failed")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
