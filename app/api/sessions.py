from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse, Response
from db.mongo import get_sessions, create_session, insert_message, get_messages
from utils.mongo_exception import (
    CollectionNotFoundError,
    MongoOperationError,
    DocumentNotFoundError
)
from models.messages import Message

router = APIRouter()

@router.get("/sessions/")
async def get_sessions_id_api(user_id: str):
    try:
        sessions = await get_sessions(user_id)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "data": sessions,
                "message": "Sessions id fetched successfully"
            }
        )
    
    except DocumentNotFoundError as e:
        return JSONResponse(content={
            "message": str(e),
            "data": None},
            status_code=404
            )
    except MongoOperationError as e:
        return JSONResponse(content={
            "message": str(e),
            "data": None},
            status_code=500
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/sessions")
async def create_session_api(user_id:str, session_name:str):
    try:
        session_id = await create_session(user_id, session_name)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "data": {"session_id": session_id},
                "message": "Session created successfully"
            }
        )
    except MongoOperationError as e:
        return JSONResponse(content={
            "message": str(e),
            "data": None},
            status_code=500
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.patch("/sessions/messages/")
async def add_message_api(user_id: str, session_id: str, message: Message):
    try:
        inserted_message_id = await insert_message(user_id, session_id, message)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "data": {"message_id": inserted_message_id},
                "message": "Message added successfully"
            }
        )
    except CollectionNotFoundError as e:
        return JSONResponse(content={
            "message": str(e),
            "data": None},
            status_code=404
            )
    except MongoOperationError as e:
        return JSONResponse(content={
            "message": str(e),
            "data": None},
            status_code=500
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/sessions/messages/")
async def get_messages_api(user_id: str, session_id: str):
    try:
        messages = await get_messages(user_id, session_id)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "data": messages,
                "message": "Messages fetched successfully"
            }
        )
    except CollectionNotFoundError as e:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "message": str(e),
                "data": None
            }
        )
    
    except DocumentNotFoundError as e:
        return Response(
            status_code=status.HTTP_204_NO_CONTENT
        )

    except MongoOperationError as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "message": str(e),
                "data": None
            }
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
    