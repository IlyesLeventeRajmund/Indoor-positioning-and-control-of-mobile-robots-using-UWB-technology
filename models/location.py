from pydantic import BaseModel
from typing import Optional


class Location(BaseModel):
    x: float
    y: float
    # Why is this optional?
    timestamp: Optional[datetime] = None