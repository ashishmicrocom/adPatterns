from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime
from bson import ObjectId


class PyObjectId(ObjectId):
    """Custom ObjectId type for Pydantic"""
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


# Base User Schema
class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    phone_number: Optional[str] = None
    company: Optional[str] = None


# User Registration Schema
class UserCreate(UserBase):
    password: str


# User Update Schema
class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    company: Optional[str] = None
    password: Optional[str] = None


# User Response Schema
class UserResponse(UserBase):
    id: str = Field(alias="_id")
    created_at: datetime
    updated_at: datetime
    is_active: bool = True
    
    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}


# User in DB Schema (with hashed password)
class UserInDB(UserBase):
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = True
    ad_accounts: List[str] = []  # List of connected ad account IDs


# Login Schema
class UserLogin(BaseModel):
    email: EmailStr
    password: str


# Token Schema
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


# Token Data
class TokenData(BaseModel):
    email: Optional[str] = None
