from datetime import datetime

from pydantic import BaseModel, Field, EmailStr


class ContactBase(BaseModel):
    first_name: str
    last_name: str


class ContactResponse(ContactBase):
    id: int
    email: str
    phone_number: str
    another_info: None

class UserModel(BaseModel):
    username: str
    email: str
    password: str

class UserDb(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime
    avatar: str

    class Config:
        orm_mode = True


class UserResponse(BaseModel):
    user: UserDb
    detail: str = "User successfully created"


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RequestEmail(BaseModel):
    email: EmailStr
