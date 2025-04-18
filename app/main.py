from uuid import uuid4
import os
import json
from fastapi import FastAPI, Form, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from db.mongo import insert_message, get_messages, get_sessions
from chatCompletion.chatcompletion import get_chat_response
from models.messages import Message, FileItem
from typing import Optional

app=FastAPI()

origins = [
    "http://localhost:3000",  # Add your frontend's URL here
    "http://127.0.0.1:3000",  # For local dev, if running on different port
]

# Add CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows your frontend origin
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

@app.post("/messages/{user_id}/{session_id}")
async def send_message(
    user_id: str,
    session_id: str,
    message: str = Form(...),  # message as JSON string
    file: Optional[UploadFile] = File(None),
):
    try:
        # Parse the message JSON string into a dict
        message_data = json.loads(message)
        msg_model = Message(**message_data)

        # Handle optional file upload
        if file:
            file_id = str(uuid4())
            file_ext = file.filename.split('.')[-1]
            unique_filename = f"{file_id}.{file_ext}"
            file_dir = os.path.join("database", "chat", user_id, session_id)
            os.makedirs(file_dir, exist_ok=True)
            file_path = os.path.join(file_dir, unique_filename)

            with open(file_path, "wb") as f_out:
                f_out.write(await file.read())

            file_item = FileItem(filename=unique_filename, file_url=file_path)

            if msg_model.files is None:
                msg_model.files = []
            msg_model.files.append(file_item)

        # Simulate DB insert
        message_id = await insert_message(user_id, session_id, msg_model.dict())
        # print(f"Inserted message: {msg_model.dict()}")

        return {
            "messageid":message_id
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


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

@app.get("/sessions/{user_id}")
async def get_sessions_api(user_id: str):
    try:
        sessions = await get_sessions(user_id)
        if not sessions:
            raise HTTPException(status_code=404, detail="No sessions found")
        return sessions
    except Exception as e:
        print("error")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI!"}


@app.post("/chat/")
async def chat(request: Message):
    # return {"received_message": request.message}
    try:
        # Call the Gemini API to get the chat completion
        response = await get_chat_response(request.text)
        print(response.text)
        return {"response": response.text}

    except Exception as e: # Logs the error in the terminal
        raise HTTPException(status_code=500, detail=f"Error: {e}")
#uvicorn main:app --reload
        