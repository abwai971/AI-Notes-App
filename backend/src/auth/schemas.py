from pydantic import BaseModel, Field, EmailStr
import uuid
from datetime import datetime
from typing import List
from pydantic import ConfigDict

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    uid: uuid.UUID
    username: str
    email: EmailStr
    first_name: str
    last_name: str 
    role: str
    is_active: bool = Field(default=True)
    created_at: datetime
    updated_at: datetime 

class UserCreateModel(BaseModel):
    first_name: str = Field(max_length=30)
    last_name: str = Field(max_length=30)
    username: str = Field(max_length=40)
    email: EmailStr
    password: str = Field(min_length=8)

class UserLoginModel(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
