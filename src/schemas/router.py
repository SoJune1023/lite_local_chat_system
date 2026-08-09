from typing import Optional, Literal, List, Dict
from pydantic import BaseModel

class InteractionRequest(BaseModel):
    message: str
    model: Literal['claude', 'ollama']

class InteractionResponse(BaseModel):
    message: str


class GetHistoryResponse(BaseModel):
    messages: Optional[List[Dict[str, str]]]