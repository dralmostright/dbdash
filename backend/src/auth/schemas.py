from pydantic import BaseModel, Field
from datetime import datetime, date
import uuid
from typing import List, Optional

class UserBaseModel(BaseModel):
    username: str = Field(max_length=32)
    email: str
    first_name: str
    last_name: str
    is_verified : Optional[bool] = None
    role : Optional[str] = None    

class UserCreateModel(UserBaseModel):
    password_hash: str = Field(max_length=64)
    
class UserPasswordData(BaseModel):
    password_hash: str = Field(max_length=64)
    new_password_hash: str = Field(max_length=64)  

class UserInfoData(BaseModel):
    first_name: str 
    last_name: str 
    email: str 
    
class UserUpdateModel(UserBaseModel):
    password_hash: Optional[str] = Field(max_length=64)

class UserCreateModelExtras(BaseModel):
    is_verified : Optional[bool] = None
    role : Optional[str] = None
    
class UserModel(BaseModel):
    uid: uuid.UUID 
    username: str
    email: str
    password_hash: str = Field(exclude=True)
    first_name: str
    last_name: str
    display_pic: str
    role: str
    is_verified: bool
    created_at: datetime
    updated_at: datetime 
    
class UserLoginModel(BaseModel):
    email: str
    password_hash: str = Field(max_length=64)