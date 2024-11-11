from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os

load_dotenv()

# Create a new client and connect to the server
client = MongoClient(os.getenv("uri"), server_api=ServerApi('1'))
db=client.user_service_db
user_collection = db['users']
profile_collection = db['profiles']

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)