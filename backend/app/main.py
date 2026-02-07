from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.config.settings import settings
from app.database.mongodb import db
from app.routes import auth_router, campaigns_router, ad_accounts_router
from app.routes.suggestions import router as suggestions_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    # Startup
    print("🚀 Starting AdPatterns API...")
    await db.connect_db()
    yield
    # Shutdown
    print("🛑 Shutting down AdPatterns API...")
    await db.close_db()


# Initialize FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Backend API for AdPatterns advertising campaign management platform",
    lifespan=lifespan,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router)
app.include_router(campaigns_router)
app.include_router(ad_accounts_router)
app.include_router(suggestions_router, prefix="/api", tags=["suggestions"])


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to AdPatterns API",
        "version": settings.app_version,
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "database": "connected" if db.client else "disconnected"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )
