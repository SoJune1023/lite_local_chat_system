from pydantic import BaseModel

class InteractionRequest(BaseModel):
    message: str

class InteractionResponse(BaseModel):
    message: str