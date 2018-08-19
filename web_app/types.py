from pymongo import MongoClient
from config import DB_PORT, DB_NAME, DB_COLLECTION_NAME

client = MongoClient(port=DB_PORT)
db = client[DB_NAME]
collection = db[DB_COLLECTION_NAME]
