from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from app.schemas.ad_account import (
    AdAccountCreate,
    AdAccountUpdate,
    AdAccountResponse,
)
from app.schemas.user import UserInDB
from app.services.auth import get_current_active_user
from app.database.mongodb import db
from bson import ObjectId
from datetime import datetime

router = APIRouter(prefix="/api/ad-accounts", tags=["Ad Accounts"])


@router.get("", response_model=List[AdAccountResponse])
async def get_ad_accounts(
    current_user: UserInDB = Depends(get_current_active_user)
):
    """Get all ad accounts for the current user"""
    ad_accounts_collection = db.get_collection("ad_accounts")
    
    # Get ad accounts
    cursor = ad_accounts_collection.find({"user_id": current_user.email})
    ad_accounts = await cursor.to_list(length=None)
    
    # Convert ObjectId to string
    for account in ad_accounts:
        account["_id"] = str(account["_id"])
    
    return [AdAccountResponse(**account) for account in ad_accounts]


@router.post("", response_model=AdAccountResponse, status_code=status.HTTP_201_CREATED)
async def connect_ad_account(
    ad_account: AdAccountCreate,
    current_user: UserInDB = Depends(get_current_active_user)
):
    """Connect a new ad account"""
    ad_accounts_collection = db.get_collection("ad_accounts")
    
    # Check if account already exists
    existing_account = await ad_accounts_collection.find_one({
        "user_id": current_user.email,
        "platform": ad_account.platform,
        "account_id": ad_account.account_id
    })
    
    if existing_account:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ad account already connected"
        )
    
    # Prepare ad account document
    account_dict = ad_account.model_dump()
    account_dict["user_id"] = current_user.email
    account_dict["status"] = "connected"
    account_dict["connected_at"] = datetime.utcnow()
    account_dict["last_sync"] = None
    account_dict["metadata"] = {}
    
    # Insert ad account
    result = await ad_accounts_collection.insert_one(account_dict)
    
    # Update user's ad_accounts list
    users_collection = db.get_collection("users")
    await users_collection.update_one(
        {"email": current_user.email},
        {"$push": {"ad_accounts": str(result.inserted_id)}}
    )
    
    # Retrieve and return created ad account
    created_account = await ad_accounts_collection.find_one({"_id": result.inserted_id})
    created_account["_id"] = str(created_account["_id"])
    
    return AdAccountResponse(**created_account)


@router.get("/{account_id}", response_model=AdAccountResponse)
async def get_ad_account(
    account_id: str,
    current_user: UserInDB = Depends(get_current_active_user)
):
    """Get a specific ad account by ID"""
    ad_accounts_collection = db.get_collection("ad_accounts")
    
    # Validate ObjectId
    if not ObjectId.is_valid(account_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid account ID"
        )
    
    # Get ad account
    account = await ad_accounts_collection.find_one({
        "_id": ObjectId(account_id),
        "user_id": current_user.email
    })
    
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ad account not found"
        )
    
    account["_id"] = str(account["_id"])
    return AdAccountResponse(**account)


@router.put("/{account_id}", response_model=AdAccountResponse)
async def update_ad_account(
    account_id: str,
    account_update: AdAccountUpdate,
    current_user: UserInDB = Depends(get_current_active_user)
):
    """Update an ad account"""
    ad_accounts_collection = db.get_collection("ad_accounts")
    
    # Validate ObjectId
    if not ObjectId.is_valid(account_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid account ID"
        )
    
    # Check if account exists and belongs to user
    existing_account = await ad_accounts_collection.find_one({
        "_id": ObjectId(account_id),
        "user_id": current_user.email
    })
    
    if not existing_account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ad account not found"
        )
    
    # Prepare update data
    update_data = account_update.model_dump(exclude_unset=True)
    
    # Update ad account
    await ad_accounts_collection.update_one(
        {"_id": ObjectId(account_id)},
        {"$set": update_data}
    )
    
    # Retrieve and return updated account
    updated_account = await ad_accounts_collection.find_one({"_id": ObjectId(account_id)})
    updated_account["_id"] = str(updated_account["_id"])
    
    return AdAccountResponse(**updated_account)


@router.delete("/{account_id}", status_code=status.HTTP_204_NO_CONTENT)
async def disconnect_ad_account(
    account_id: str,
    current_user: UserInDB = Depends(get_current_active_user)
):
    """Disconnect an ad account"""
    ad_accounts_collection = db.get_collection("ad_accounts")
    
    # Validate ObjectId
    if not ObjectId.is_valid(account_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid account ID"
        )
    
    # Delete ad account
    result = await ad_accounts_collection.delete_one({
        "_id": ObjectId(account_id),
        "user_id": current_user.email
    })
    
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ad account not found"
        )
    
    # Remove from user's ad_accounts list
    users_collection = db.get_collection("users")
    await users_collection.update_one(
        {"email": current_user.email},
        {"$pull": {"ad_accounts": account_id}}
    )
    
    return None
