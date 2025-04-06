from pydantic import BaseModel   

class DistanceInput(BaseModel):
    distance: float