from django.db import connections
import pymongo
from config.settings import MONGO_HOST, MONGO_PORT, MONGO_NAME, MONGO_USERNAME, MONGO_PASSWORD


CROSS_DATA_COLLECTION = 'cross_data'
LONG_DATA_COLLECTION = 'long_data'
RF_RESULT = 'rf_result'
Y_RESULT = 'y_result'
MERGED_DATA = 'merged_data'

MONGO_AUTH = f"{MONGO_USERNAME}:{MONGO_PASSWORD}@" if MONGO_USERNAME else ""
MONGO_URI = "mongodb://" + MONGO_AUTH + MONGO_HOST + ":" + MONGO_PORT

client = pymongo.MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
# Test connection
client.admin.command('ping')

def get_db():
    """
    Returns the native PyMongo database object from Djongo connection.
    """
    return client[MONGO_NAME]


def get_collection(collection_name):
    """
    Shortcut to get a specific collection.
    """
    db = get_db()
    return db[collection_name]