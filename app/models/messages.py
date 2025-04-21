from pydantic import BaseModel
from typing import List, Union, Optional
from datetime import datetime

class DesiredOutput(BaseModel):
    id: Optional[str] = None
    title: str    
    description: Optional[str] = None
    type: Optional[str] = None
    path: str

class AgentItem(BaseModel):
    name: str    
    role: str
    prompt: str
    model: str
    avatar: str

class OutputFiles(BaseModel):
    id: Optional[str] = None
    title: str    
    description: Optional[str] = None
    type: Optional[str] = None
    path: str

class Message(BaseModel):
    message_id: Optional[str] = None
    text: str = None  # Text content of the message
    # sender: Optional[str] = None  # Sender's name or ID
    desired_output: Optional[List[DesiredOutput]] = None  # List of attached files
    agents: Optional[List[AgentItem]] = None  # Card content of the message
    timestamp: Optional[datetime] = datetime.now()  # Using datetime directly
    output_files:Optional[List[OutputFiles]] = None
    type: Optional[str] = None  # Possible values: 'text', 'image with text', 'file with text', 'card with text'


class Sessions(BaseModel):
    session_id: str
    session_name: str
    messages: List[Message]