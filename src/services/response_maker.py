import os
import logging

from typing import List, Dict
from ollama import AsyncClient, ResponseError

logger = logging.getLogger(__name__)

MODEL = os.getenv('OLLAMA_MODEL')

class ResponseMaker:
    async def _get_response(
        self,
        history: List[Dict[str, str]]
    ) -> str:
        try:
            response = await AsyncClient().chat(
                model=MODEL,
                messages=history
            )

            return response['message']['content']
        except ResponseError as e:
            logger.error(f"Could not get response from ollama")
            raise e

    async def run(
        self,
        history: List[Dict[str, str]]
    ) -> str:
        response = await self._get_response(history)
        return response