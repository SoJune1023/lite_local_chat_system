from typing import Literal
from pydantic import BaseModel

class InteractionRequest(BaseModel):
    message: str
    model: Literal['claude', 'ollama']

class InteractionResponse(BaseModel):
    message: str