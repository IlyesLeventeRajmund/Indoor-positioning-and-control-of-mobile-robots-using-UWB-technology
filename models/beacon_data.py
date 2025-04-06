from pydantic import BaseModel
from typing import Dict

class BeaconData(BaseModel):
    beacon1: Dict[str, float]
    beacon2: Dict[str, float]
    beacon3: Dict[str, float]
    beacon4: Dict[str, float]