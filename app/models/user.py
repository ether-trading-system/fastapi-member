from datetime import date
from typing import Optional

class User:
    def __init__(self, access_token: str, expired_date: date, access_token_type: str, expires_in: int):
        self.access_token = access_token
        self.expired_date = expired_date
        self.access_token_type = access_token_type
        self.expires_in = expires_in

    def __repr__(self):
        return f"User(access_token={self.access_token}, expired_date={self.expired_date}, access_token_type={self.access_token_type}, expires_in={self.expires_in})"