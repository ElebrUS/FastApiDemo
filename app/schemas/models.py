from datetime import datetime
from enum import Enum

from functions import hash_password
from pydantic import BaseModel, EmailStr, Field, validator


class UserModel(BaseModel):
    id: int = None
    username: str
    email: EmailStr
    password: str
    register_date: datetime = Field(default_factory=datetime.now)

    @validator('password')
    def hash_password(cls, pw: str) -> str:
        return hash_password(pw)

    class Config:
        orm_mode = True


class UserInModel(UserModel):
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True

        schema_extra = {
            'example': {
                'username': 'ElebrUS',
                'email': 'elebrus@example.com',
                'password': 'p@ssword',
            }
        }


class UserUpdatePassword(BaseModel):
    user_id: int
    old_password: str
    new_password: str

    @validator('new_password')
    def hash_password(cls, pw: str) -> str:
        return hash_password(pw)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True

        schema_extra = {
            'example': {
                'user_id': 1,
                'old_password': 'p@ssword',
                'new_password': 'New-p@ssword',
            }
        }


class GetAllUserModel(BaseModel):
    count: int = 100
    start: int = 0


class SearchEnum(str, Enum):
    user_id = 'user_id'
    username = 'username'
    email = 'email'


class SearchModel(BaseModel):
    field: SearchEnum = SearchEnum.username
    search_text: str = 'User'

