from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime
from enum import Enum


class AdAccountPlatform(str, Enum):
    META = "meta"
    GOOGLE = "google"
    LINKEDIN = "linkedin"
    TWITTER = "twitter"


class AdAccountStatus(str, Enum):
    CONNECTED = "connected"
    DISCONNECTED = "disconnected"
    ERROR = "error"
    PENDING = "pending"


# Base Ad Account Schema
class AdAccountBase(BaseModel):
    platform: AdAccountPlatform
    account_id: str
    account_name: str
    currency: str = "USD"


# Ad Account Create Schema
class AdAccountCreate(AdAccountBase):
    access_token: str
    refresh_token: Optional[str] = None
    permissions: Optional[Dict[str, bool]] = None


# Ad Account Update Schema
class AdAccountUpdate(BaseModel):
    account_name: Optional[str] = None
    status: Optional[AdAccountStatus] = None
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
    permissions: Optional[Dict[str, bool]] = None


# Ad Account Response Schema
class AdAccountResponse(AdAccountBase):
    id: str = Field(alias="_id")
    user_id: str
    status: AdAccountStatus
    permissions: Optional[Dict[str, bool]] = None
    connected_at: datetime
    last_sync: Optional[datetime] = None
    
    class Config:
        populate_by_name = True
        use_enum_values = True


# Ad Account in DB Schema
class AdAccountInDB(AdAccountBase):
    user_id: str
    access_token: str
    refresh_token: Optional[str] = None
    status: AdAccountStatus = AdAccountStatus.CONNECTED
    permissions: Optional[Dict[str, bool]] = {
        "ads_management": True,
        "ads_read": True,
        "pages_read_engagement": False,
    }
    connected_at: datetime = Field(default_factory=datetime.utcnow)
    last_sync: Optional[datetime] = None
    metadata: Optional[Dict[str, Any]] = None


# Ad Account Connection Request
class AdAccountConnect(BaseModel):
    platform: AdAccountPlatform
    authorization_code: str
