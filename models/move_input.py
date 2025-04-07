from pydantic import BaseModel

class MoveInput(BaseModel):
    direction: str

    # TODO: Add validation for direction