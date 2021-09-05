from pymongo import MongoClient
from config import DB_HOST, DB_PORT, DB_NAME, DB_COLLECTION_NAME

client = MongoClient(host=DB_HOST, port=DB_PORT)
db = client[DB_NAME]
collection = db[DB_COLLECTION_NAME]
