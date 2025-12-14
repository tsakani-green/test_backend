# db.py
from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_URI, MONGO_DB_NAME

client: AsyncIOMotorClient = AsyncIOMotorClient(MONGO_URI)
db = client[MONGO_DB_NAME]

users_collection = db["users"]
organisations_collection = db["organisations"]
sites_collection = db["sites"]
invoices_collection = db["invoices"]
metrics_collection = db["environmental_metrics"]
