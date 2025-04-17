from pydantic import BaseModel
from typing import List, Union, Optional
from datetime import datetime

class FileItem(BaseModel):
    filename: str
    file_url: str

class CardItem(BaseModel):
    title: str
    description: Optional[str] = None
    button_text: Optional[str] = None
    button_url: Optional[str] = None

class Content(BaseModel):
    type: str  # Possible values: 'text', 'image with text', 'file with text', 'card with text'
    text: Optional[str] = None
    files: Optional[List[FileItem]] = None
    image_url: Optional[str] = None
    card: Optional[CardItem] = None

class Message(BaseModel):
    sender: str
    timestamp: Optional[datetime] = datetime.now()  # Using datetime directly
    content: Content
