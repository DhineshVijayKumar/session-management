from pydantic import BaseModel
from typing import List, Union, Optional
from datetime import datetime

class FileItem(BaseModel):
    filename: str
    file_url: str

class CardItem(BaseModel):
    title: str
    description: Optional[List[str]] = None
    button_text: Optional[List[str]] = None
    button_url: Optional[List[str]] = None

class Message(BaseModel):
    sender: Optional[str] = None  # Sender's name or ID
    timestamp: Optional[datetime] = datetime.now()  # Using datetime directly
    type: Optional[str] = None  # Possible values: 'text', 'image with text', 'file with text', 'card with text'
    text: str = None  # Text content of the message
    files: Optional[List[FileItem]] = None  # List of attached files
    card: Optional[CardItem] = None  # Card content of the message
