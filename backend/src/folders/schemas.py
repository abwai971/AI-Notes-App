from pydantic import BaseModel, Field, EmailStr
import uuid
from datetime import datetime
from typing import List, Optional
from pydantic import ConfigDict

class Folder(BaseModel):
    uid : uuid.UUID
    name : str
    description: Optional[str] = None 
    color: str
    created_at: datetime
    updated_at: datetime

class createFolderModel(BaseModel):
    name : str
    description: Optional[str] = None
    color : str

class updateFolderModel(BaseModel):
    name: Optional[str] = None
    color: Optional[str] = None
    description: Optional[str] = None