import os
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from utils.mongo_exception import CollectionNotFoundError, MongoOperationError, DocumentNotFoundError
from utils.helpers import timestampToISOFormat
from pymongo.errors import PyMongoError
from dotenv import load_dotenv
from typing import Dict, List
from models.messages import Message
from uuid import uuid4

# Load environment variables from .env file
load_dotenv()

# MongoDB URI
MONGO_URI = os.getenv("MONGO_URI")
client = AsyncIOMotorClient(MONGO_URI)

async def create_session(user_id:str, session_name:str):
    try:
        db = client[user_id]
        collection = db["session"]

        session_id = str(uuid4())
        await collection.insert_one({
            "session_id": session_id,
            "session_name": session_name,
            "messages": []
        })
        return session_id

    except PyMongoError as e:
        raise MongoOperationError(f"Database error: {str(e)}")

async def get_sessions(user_id: str):
    try:
        db = client[user_id]
        collection = db["session"]
        sessions_cursor = collection.find({}, {"session_id": 1, "session_name": 1, "_id": 0})
        sessions = await sessions_cursor.to_list(length=None)  # length=None returns all results
        if not sessions:
            raise DocumentNotFoundError(f"User has no sessions.")
        
        return sessions

    except PyMongoError as e:
        raise MongoOperationError(f"Database error: {str(e)}")

    
async def insert_message(user_id: str, session_id: str, msg: Message) -> str:
    try:
        db = client[user_id]
        collection = db["session"]
        msg_dict = msg.dict()

        session_exists = await collection.find_one({"session_id": session_id})
        if not session_exists:
            raise CollectionNotFoundError(f"Session '{session_id}' not found in database.")
        
        msg_id = str(uuid4())
        msg_dict["message_id"] = msg_id
        result = await collection.update_one(
                {"session_id": session_id},  # filter
                {"$push": {"messages": msg_dict}}  # push to array field
            ) 

        if result.modified_count == 0:
            raise MongoOperationError("Message was not inserted.")

        return msg_id
    
    except PyMongoError as e:
        raise MongoOperationError(f"Database error: {str(e)}")
    
async def get_messages(user_id: str, session_id: str):
    try:
        db = client[user_id]
        collection = db["session"]
        
        session_doc = await collection.find_one({"session_id": session_id}, {"_id": 0})
        
        if not session_doc:
            raise CollectionNotFoundError(f"Session '{session_id}' not found.")

        messages_list = session_doc.get("messages", [])
        # return {"messages": messages_list}
        if not messages_list:
            raise DocumentNotFoundError(f"Session '{session_id}' has no messages.")

        for msg in messages_list:
            if "timestamp" in msg:
                msg["timestamp"] = timestampToISOFormat(msg["timestamp"])
        
        return session_doc
    except PyMongoError as e:
        raise MongoOperationError(f"Database error: {str(e)}")
