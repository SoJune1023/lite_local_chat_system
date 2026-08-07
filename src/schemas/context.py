from pydantic import BaseModel
from typing import Optional, Any

class History(BaseModel):
    history: Optional[Any] = None 