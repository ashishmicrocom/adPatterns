from motor.motor_asyncio import AsyncIOMotorClient
from app.config.settings import settings
from typing import Optional


class MongoDB:
    client: Optional[AsyncIOMotorClient] = None
    
    @classmethod
    async def connect_db(cls):
        """Connect to MongoDB Atlas"""
        try:
            cls.client = AsyncIOMotorClient(settings.mongodb_url)
            # Ping the database to verify connection
            await cls.client.admin.command('ping')
            print(f"✅ Connected to MongoDB Atlas - Database: {settings.database_name}")
        except Exception as e:
            print(f"❌ Error connecting to MongoDB: {e}")
            raise
    
    @classmethod
    async def close_db(cls):
        """Close MongoDB connection"""
        if cls.client:
            cls.client.close()
            print("🔌 Disconnected from MongoDB")
    
    @classmethod
    def get_database(cls):
        """Get database instance"""
        if not cls.client:
            raise Exception("Database not connected. Call connect_db() first.")
        return cls.client[settings.database_name]
    
    @classmethod
    def get_collection(cls, collection_name: str):
        """Get collection by name"""
        db = cls.get_database()
        return db[collection_name]


# Database instance
db = MongoDB()


# Helper function to get database
def get_db():
    return db.get_database()
