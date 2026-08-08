import os
import logging

from typing import List, Dict
from ollama import AsyncClient, ResponseError, ChatResponse

from src.tools.web_search import web_search

logger = logging.getLogger(__name__)

MODEL = os.getenv('OLLAMA_MODEL')
MAX_ROUNDS = 5

class Ollama:
    _client: AsyncClient

    def __init__(self):
        self._client = AsyncClient()

    async def _get_response(
        self,
        history: List[Dict[str, str]]
    ) -> str:
        for _ in range(MAX_ROUNDS):
            try:
                response: ChatResponse = await self._client.chat(
                    model=MODEL,
                    messages=history,
                    tools=[web_search],
                )
            except ResponseError as e:
                logger.error(f"Could not get response from ollama")
                raise RuntimeError(f"Could not get response from ollama") from e

            if not response.message.tool_calls:
                return response.message.content

            history.append(response.message)

            for tool in response.message.tool_calls:
                if tool.function.name == 'web_search':
                    try:
                        result = web_search(**tool.function.arguments)
                    except Exception as e:
                        logger.error(f"Web search failed.")
                        raise RuntimeError(f"Web search failed.") from e
                else:
                    logger.error(f"Unknown tool: {tool.function.name}")
                    raise RuntimeError(f"Unknown tool: {tool.function.name}")

                history.append({
                    'role': 'tool',
                    'content': result,
                    'tool_name': tool.function.name,
                })

        raise RuntimeError(f"Tool call loop exceeded {MAX_ROUNDS} rounds")

    async def run(
        self,
        history: List[Dict[str, str]]
    ) -> str:
        response = await self._get_response(history)
        return response