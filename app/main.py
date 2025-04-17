from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import  List, Dict
from db.mongo import insert_message, get_messages
from models.messages import Message

app=FastAPI()

@app.post("/messages/{user_id}/{session_id}")
async def send_message(user_id: str, session_id: str, message: Message):
    try:
        # Convert Message model to dictionary for MongoDB insertion
        msg_dict = message.dict()
        
        # Insert the message into MongoDB
        message_id = await insert_message(user_id, session_id, msg_dict)
        
        return {"message_id": message_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/messages/{user_id}/{session_id}")
async def get_messages_api(user_id: str, session_id: str):
    try:
        messages = await get_messages(user_id, session_id)
        if not messages:
            raise HTTPException(status_code=404, detail="No messages found")
        return messages
    except Exception as e:
        print("error")
        raise HTTPException(status_code=500, detail=str(e))


#uvicorn main:app --reload
        