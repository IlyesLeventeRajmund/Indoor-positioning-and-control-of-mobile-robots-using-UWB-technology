from pydantic import BaseModel

class MoveInput(BaseModel):
    direction: str