from pydantic import BaseModel, Field


# F/E(React) >> Member/Account Server : Access Token 발급 요청 Payload 타입
class KakaoTokenRequest(BaseModel):
    grant_type: str = Field(default="authorization_code", Literal=True)   # authorization_code 고정
    client_id: str                                                      # REST API 키
    redirect_uri: str                                                   # 인가코드가 Redirect된 URI
    code: str                                                           # 인가코드 받기 요청으로 얻은 인가코드
    refresh_token: str
    client_secret: str = None                                           # 보안 강화용, 필수 X


# Kakao API Server >> FastAPI Server : Access Token 본문 타입
class KakaoTokenResponse(BaseModel):
    token_type: str
    access_token: str
    id_token: str = None
    expires_in: int
    refresh_token: str 
    refresh_token_expires_in: int
    scope: str = None
    

# FastAPI Server >> Kakao API Server : Access Token 방식의 Logout 요청 타입
class KakaoLogoutRequest(BaseModel):
    access_token: str
    target_id: int
