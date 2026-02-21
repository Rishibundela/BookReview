import uuid
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class TagModel(BaseModel):
    id: uuid.UUID
    name: str
    created_at: Optional[datetime] = None


class TagCreateModel(BaseModel):
    name: str


class TagAddModel(BaseModel):
    tags: List[TagCreateModel]