from app.routes.auth import router as auth_router
from app.routes.campaigns import router as campaigns_router
from app.routes.ad_accounts import router as ad_accounts_router

__all__ = ["auth_router", "campaigns_router", "ad_accounts_router"]
