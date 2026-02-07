from fastapi import APIRouter, HTTPException, status, Depends, Query
from typing import List, Optional
from app.schemas.campaign import (
    CampaignCreate,
    CampaignUpdate,
    CampaignResponse,
    CampaignSummary,
    CampaignStatus,
)
from app.schemas.user import UserInDB
from app.services.auth import get_current_active_user
from app.database.mongodb import db
from bson import ObjectId
from datetime import datetime

router = APIRouter(prefix="/api/campaigns", tags=["Campaigns"])


@router.get("", response_model=List[CampaignResponse])
async def get_campaigns(
    status: Optional[CampaignStatus] = None,
    platform: Optional[str] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    current_user: UserInDB = Depends(get_current_active_user)
):
    """Get all campaigns for the current user"""
    campaigns_collection = db.get_collection("campaigns")
    
    # Build query
    query = {"user_id": current_user.email}
    if status:
        query["status"] = status
    if platform:
        query["platform"] = platform
    
    # Get campaigns
    cursor = campaigns_collection.find(query).skip(skip).limit(limit)
    campaigns = await cursor.to_list(length=limit)
    
    # Convert ObjectId to string
    for campaign in campaigns:
        campaign["_id"] = str(campaign["_id"])
    
    return [CampaignResponse(**campaign) for campaign in campaigns]


@router.post("", response_model=CampaignResponse, status_code=status.HTTP_201_CREATED)
async def create_campaign(
    campaign: CampaignCreate,
    current_user: UserInDB = Depends(get_current_active_user)
):
    """Create a new campaign"""
    campaigns_collection = db.get_collection("campaigns")
    
    # Prepare campaign document
    campaign_dict = campaign.model_dump()
    campaign_dict["user_id"] = current_user.email
    campaign_dict["created_at"] = datetime.utcnow()
    campaign_dict["updated_at"] = datetime.utcnow()
    campaign_dict["metrics"] = {
        "impressions": 0,
        "clicks": 0,
        "conversions": 0,
        "spend": 0.0,
        "ctr": 0.0,
        "cpc": 0.0,
    }
    
    # Insert campaign
    result = await campaigns_collection.insert_one(campaign_dict)
    
    # Retrieve and return created campaign
    created_campaign = await campaigns_collection.find_one({"_id": result.inserted_id})
    created_campaign["_id"] = str(created_campaign["_id"])
    
    return CampaignResponse(**created_campaign)


@router.get("/{campaign_id}", response_model=CampaignResponse)
async def get_campaign(
    campaign_id: str,
    current_user: UserInDB = Depends(get_current_active_user)
):
    """Get a specific campaign by ID"""
    campaigns_collection = db.get_collection("campaigns")
    
    # Validate ObjectId
    if not ObjectId.is_valid(campaign_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid campaign ID"
        )
    
    # Get campaign
    campaign = await campaigns_collection.find_one({
        "_id": ObjectId(campaign_id),
        "user_id": current_user.email
    })
    
    if not campaign:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campaign not found"
        )
    
    campaign["_id"] = str(campaign["_id"])
    return CampaignResponse(**campaign)


@router.put("/{campaign_id}", response_model=CampaignResponse)
async def update_campaign(
    campaign_id: str,
    campaign_update: CampaignUpdate,
    current_user: UserInDB = Depends(get_current_active_user)
):
    """Update a campaign"""
    campaigns_collection = db.get_collection("campaigns")
    
    # Validate ObjectId
    if not ObjectId.is_valid(campaign_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid campaign ID"
        )
    
    # Check if campaign exists and belongs to user
    existing_campaign = await campaigns_collection.find_one({
        "_id": ObjectId(campaign_id),
        "user_id": current_user.email
    })
    
    if not existing_campaign:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campaign not found"
        )
    
    # Prepare update data
    update_data = campaign_update.model_dump(exclude_unset=True)
    update_data["updated_at"] = datetime.utcnow()
    
    # Update campaign
    await campaigns_collection.update_one(
        {"_id": ObjectId(campaign_id)},
        {"$set": update_data}
    )
    
    # Retrieve and return updated campaign
    updated_campaign = await campaigns_collection.find_one({"_id": ObjectId(campaign_id)})
    updated_campaign["_id"] = str(updated_campaign["_id"])
    
    return CampaignResponse(**updated_campaign)


@router.delete("/{campaign_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_campaign(
    campaign_id: str,
    current_user: UserInDB = Depends(get_current_active_user)
):
    """Delete a campaign"""
    campaigns_collection = db.get_collection("campaigns")
    
    # Validate ObjectId
    if not ObjectId.is_valid(campaign_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid campaign ID"
        )
    
    # Delete campaign
    result = await campaigns_collection.delete_one({
        "_id": ObjectId(campaign_id),
        "user_id": current_user.email
    })
    
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campaign not found"
        )
    
    return None


@router.get("/summary/stats", response_model=CampaignSummary)
async def get_campaign_summary(
    current_user: UserInDB = Depends(get_current_active_user)
):
    """Get campaign summary statistics"""
    campaigns_collection = db.get_collection("campaigns")
    
    # Get all user campaigns
    campaigns = await campaigns_collection.find({"user_id": current_user.email}).to_list(length=None)
    
    # Calculate summary
    total_campaigns = len(campaigns)
    active_campaigns = len([c for c in campaigns if c.get("status") == "active"])
    
    total_spend = sum(c.get("metrics", {}).get("spend", 0) for c in campaigns)
    total_impressions = sum(c.get("metrics", {}).get("impressions", 0) for c in campaigns)
    total_clicks = sum(c.get("metrics", {}).get("clicks", 0) for c in campaigns)
    
    average_ctr = (total_clicks / total_impressions * 100) if total_impressions > 0 else 0
    
    return CampaignSummary(
        total_campaigns=total_campaigns,
        active_campaigns=active_campaigns,
        total_spend=total_spend,
        total_impressions=total_impressions,
        total_clicks=total_clicks,
        average_ctr=round(average_ctr, 2)
    )


@router.post("/{campaign_id}/publish", response_model=CampaignResponse)
async def publish_campaign(
    campaign_id: str,
    current_user: UserInDB = Depends(get_current_active_user)
):
    """Publish a campaign (change status from draft to active)"""
    campaigns_collection = db.get_collection("campaigns")
    
    # Validate ObjectId
    if not ObjectId.is_valid(campaign_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid campaign ID"
        )
    
    # Check if campaign exists and belongs to user
    existing_campaign = await campaigns_collection.find_one({
        "_id": ObjectId(campaign_id),
        "user_id": current_user.email
    })
    
    if not existing_campaign:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campaign not found"
        )
    
    # Check if campaign is already active
    if existing_campaign.get("status") == "active":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Campaign is already active"
        )
    
    # Update campaign status to active
    update_data = {
        "status": "active",
        "updated_at": datetime.utcnow()
    }
    
    # Set start date to now if not set
    if not existing_campaign.get("start_date"):
        update_data["start_date"] = datetime.utcnow()
    
    await campaigns_collection.update_one(
        {"_id": ObjectId(campaign_id)},
        {"$set": update_data}
    )
    
    # Retrieve and return published campaign
    published_campaign = await campaigns_collection.find_one({"_id": ObjectId(campaign_id)})
    published_campaign["_id"] = str(published_campaign["_id"])
    
    return CampaignResponse(**published_campaign)
