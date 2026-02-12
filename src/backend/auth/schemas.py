from pydantic import BaseModel
from typing import Optional

class Token(BaseModel):
    access_token: str
    refresh_token: str          # New field
    token_type: str
    role: str
    access_token_expires_in: int  # Duration in seconds
    refresh_token_expires_in: int # Duration in seconds

class TokenData(BaseModel):
    username: Optional[str] = None
    role: Optional[str] = None

class User(BaseModel):
    username: str
    role: str

class UserInDB(User):
    hashed_password: str