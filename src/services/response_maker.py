import os
import logging

from typing import List, Dict, Literal

from src.clients.claude import Claude
from src.clients.ollama import Ollama

logger = logging.getLogger(__name__)

MODEL = os.getenv('OLLAMA_MODEL')
MAX_ROUNDS = 5

class ResponseMaker:
    _model: Literal['ollama', 'claude']

    def __init__(
        self,
        model: Literal['ollama', 'claude']
    ) -> None:
        self._model = model

    async def _get_response(
        self,
        history: List[Dict[str, str]]
    ) -> str:
        if self._model == 'claude':
            responser = Claude()
            response = await responser.run(history)
        elif self._model == 'ollama':
            responser = Ollama()
            response = await responser.run(history)
        else:
            raise RuntimeError(f"Unknown model: {self._model}")

        return response
        
    async def run(
        self,
        history: List[Dict[str, str]]
    ) -> str:
        response = await self._get_response(history)
        return response