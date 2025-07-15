from django.db import connections


CROSS_DATA_COLLECTION = 'cross_data'
LONG_DATA_COLLECTION = 'long_data'
RF_RESULT = 'rf_result'
Y_RESULT = 'y_result'
MERGED_DATA = 'merged_data'


def get_db(alias='default'):
    """
    Returns the native PyMongo database object from Djongo connection.
    """
    return connections[alias].connection


def get_collection(collection_name, alias='default'):
    """
    Shortcut to get a specific collection.
    """
    db = get_db(alias)
    return db[collection_name]