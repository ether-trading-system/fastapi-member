from pydantic import BaseModel, Field

class TokenRequest(BaseModel):
    grant_type: str = Field(default="authorization_code", Literal=True)   # authorization_code 고정
    client_id: str                                                      # REST API 키
    redirect_uri: str                                                   # 인가코드가 Redirect된 URI
    code: str                                                           # 인가코드 받기 요청으로 얻은 인가코드
    client_secret: str = None                                           # 보안 강화용, 필수 X


class TokenResponse(BaseModel):
    token_type: str
    access_token: str
    id_token: str = None
    expires_in: int
    refresh_token: str 
    refresh_token_expires_in: int
    scope: str = None