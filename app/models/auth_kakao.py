import datetime
from typing import Optional


class TokenRequest:
    def __init__(self, grant_type: str, client_id: int, redirect_uri: str, code: str, client_secret: str):
        self.grant_type = grant_type
        self.client_id = client_id
        self.redirect_uri = redirect_uri
        self.code = code
        self.client_secret = client_secret

    def __repr__(self):
        return f"TokenRequest(grant_type={self.grant_type}, client_id={self.client_id}, redirect_uri={self.redirect_uri}, code={self.code}, client_secret={self.client_secret})"
    

class TokenResponse:
    def __init__(self, token_type: str, access_token: str, id_token: str, expires_in: int, refresh_token: str, refresh_token_expires_in: int, scope: str):
        self.token_type = token_type
        self.access_token = access_token
        self.id_token = id_token
        self.expires_in = expires_in
        
        self.refresh_token = refresh_token
        self.refresh_token_expires_in = refresh_token_expires_in
        self.scope = scope

    def __repr__(self):
        return f"TokenResponse(token_type={self.token_type}, access_token={self.access_token}, id_token={self.id_token}, expires_in={self.expires_in}, refresh_token={self.refresh_token}, refresh_token_expires_in={self.refresh_token_expires_in}, scope={self.scope})"
    


class KakaoLoginUserInfo:
    def __init__(self, service_type: str
                , user_id: str
                , nickname: str
                , name: str
                , profile_image: str
                , thumbnail_image: str
                , email_address: str
                , connected_at: datetime

                , access_token: str
                , token_type: str
                , refresh_token: str
                , expires_in: int
                , scope: str
                , refresh_token_expires_in: int

                , create_date: datetime
                , create_by: str
                , modify_date: datetime
                , modify_by: str):
        
        self.service_type = service_type
        self.user_id = user_id
        self.nickname = nickname
        self.name = name
        self.profile_image = profile_image
        self.thumbnail_image = thumbnail_image
        self.email_address = email_address
        self.connected_at = connected_at

        self.access_token = access_token
        self.token_type = token_type
        self.refresh_token = refresh_token
        self.expires_in = expires_in
        self.scope = scope
        self.refresh_token_expires_in = refresh_token_expires_in

        self.create_date = create_date
        self.create_by = create_by
        self.modify_date = modify_date
        self.modify_by = modify_by

    def __repr__(self):
        return f"KakaoLoginUserInfo Init"