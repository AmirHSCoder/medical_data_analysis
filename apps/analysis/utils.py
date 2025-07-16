import motor.motor_asyncio
from config.settings import (
    MONGO_HOST,
    MONGO_PORT,
    MONGO_NAME,
    MONGO_USERNAME,
    MONGO_PASSWORD,
)


CROSS_DATA_COLLECTION = 'cross_data'
LONG_DATA_COLLECTION = 'long_data'
RF_RESULT = 'rf_result'
Y_RESULT = 'y_result'
MERGED_DATA = 'merged_data'

MONGO_AUTH = f"{MONGO_USERNAME}:{MONGO_PASSWORD}@" if MONGO_USERNAME else ""
MONGO_URI = "mongodb://" + MONGO_AUTH + MONGO_HOST + ":" + MONGO_PORT
USE_ASYNC_DB = True

client = None

def _init_client():
    global client
    if client is None:
        client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        client.admin.command("ping")


sync_client = None

def _init_sync_client():
    global sync_client
    if sync_client is None:
        import pymongo
        sync_client = pymongo.MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        sync_client.admin.command("ping")


def get_db():
    """
    Returns the native PyMongo database object from Djongo connection.
    """
    if USE_ASYNC_DB:
        _init_client()
        db = client
    else:
        _init_sync_client()
        db = sync_client
    
    return db[MONGO_NAME]


def get_collection(collection_name):
    """
    Shortcut to get a specific collection.
    """
    db = get_db()
    return db[collection_name]