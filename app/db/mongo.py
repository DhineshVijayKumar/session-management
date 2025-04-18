import os
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from typing import Dict, List

# Load environment variables from .env file
load_dotenv()

# MongoDB URI
MONGO_URI = os.getenv("MONGO_URI")
client = AsyncIOMotorClient(MONGO_URI)

async def insert_message(user_id: str, session_id: str, msg: Dict) -> str:
    db = client[user_id]
    collection = db[session_id]
    result = await collection.insert_one(msg)
    return str(result.inserted_id)

async def get_messages(user_id: str, session_id: str) -> List[Dict]:
    db = client[user_id]
    collection = db[session_id]
    
    # No need to check if the collection exists because MongoDB handles it for you
    cursor = collection.find({})
    messages = []
    async for doc in cursor:
        doc["_id"] = str(doc["_id"])  # Convert ObjectId to string
        messages.append(doc)
    
    if not messages:
        return [{"error": "No messages found"}]
    
    return messages

#get user sessions
async def get_sessions(user_id: str) -> List[str]:
    try:
        db = client[user_id]
        collections = await db.list_collection_names()


        return collections
    except Exception as e:
        return {
            "error": str(e)
        }
    
# Function to get the MongoDB client
async def get_mongo_client():
    try:
        client = AsyncIOMotorClient(MONGO_URI)
        # Test if the client is connected by listing the databases
        await client.server_info()  # This will raise an error if the connection fails
        return client
    except Exception as e:
        print(f"Failed to connect to MongoDB: {e}")
        return None
        client = AsyncIOMotorClient(MONGO_URI)
        # Test if the client is connected by listing the databases
        await client.server_info()  # This will raise an error if the connection fails
        return client
    except Exception as e:
        print(f"Failed to connect to MongoDB: {e}")
        return None

# Function to test the MongoDB connection
async def test_connection():
    client = await get_mongo_client()  # Get the MongoDB client
    if client:
        try:
            # List all databases
            db_names = await client.list_database_names()
            
            if db_names:
                print("Databases found:", db_names)
            else:
                print("No databases found.")
        except Exception as e:
            print(f"Error fetching databases: {e}")
    else:
        print("Failed to connect to MongoDB.")


if __name__ == "__main__":

    sessions = asyncio.run(get_sessions("user12"))
    print(sessions)
    
    # messages = asyncio.run(get_messages("user1", "session1"))
    # print(messages)
    
    # asyncio.run(test_connection())

    # asyncio.run(insert_message("user1", "session1", {"message": "Hello"}))
