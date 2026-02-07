from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class PlatformType(str, Enum):
    META = "meta"
    GOOGLE = "google"
    LINKEDIN = "linkedin"
    TWITTER = "twitter"


class CampaignStatus(str, Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    ARCHIVED = "archived"


class CampaignObjective(str, Enum):
    AWARENESS = "awareness"
    TRAFFIC = "traffic"
    ENGAGEMENT = "engagement"
    LEADS = "leads"
    SALES = "sales"
    APP_PROMOTION = "app_promotion"


# Base Campaign Schema
class CampaignBase(BaseModel):
    name: str
    platform: PlatformType
    objective: CampaignObjective
    budget: float
    budget_type: str = "daily"  # daily or lifetime
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    status: CampaignStatus = CampaignStatus.DRAFT


# Campaign Create Schema
class CampaignCreate(CampaignBase):
    ad_account_id: str
    targeting: Optional[Dict[str, Any]] = None
    ad_creative: Optional[Dict[str, Any]] = None


# Campaign Update Schema
class CampaignUpdate(BaseModel):
    name: Optional[str] = None
    objective: Optional[CampaignObjective] = None
    budget: Optional[float] = None
    budget_type: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    status: Optional[CampaignStatus] = None
    targeting: Optional[Dict[str, Any]] = None
    ad_creative: Optional[Dict[str, Any]] = None


# Campaign Response Schema
class CampaignResponse(CampaignBase):
    id: str = Field(alias="_id")
    user_id: str
    ad_account_id: str
    targeting: Optional[Dict[str, Any]] = None
    ad_creative: Optional[Dict[str, Any]] = None
    metrics: Optional[Dict[str, Any]] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        populate_by_name = True
        use_enum_values = True


# Campaign in DB Schema
class CampaignInDB(CampaignBase):
    user_id: str
    ad_account_id: str
    targeting: Optional[Dict[str, Any]] = None
    ad_creative: Optional[Dict[str, Any]] = None
    metrics: Optional[Dict[str, Any]] = {
        "impressions": 0,
        "clicks": 0,
        "conversions": 0,
        "spend": 0.0,
        "ctr": 0.0,
        "cpc": 0.0,
    }
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


# Campaign Summary for Dashboard
class CampaignSummary(BaseModel):
    total_campaigns: int
    active_campaigns: int
    total_spend: float
    total_impressions: int
    total_clicks: int
    average_ctr: float
