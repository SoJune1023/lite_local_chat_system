import os
import logging
import anthropic

from typing import List, Dict
from pydantic import BaseModel

logger = logging.getLogger(__name__)

ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
MODEL = os.getenv('ANTHROPIC_MODEL')
MAX_ROUNDS = 5

class Claude:
    class ExtractedPrompt(BaseModel):
        prompt: str
        messages: List[Dict[str, str]]

    _client: anthropic.AsyncAnthropic

    def __init__(self):
        self._client = anthropic.AsyncAnthropic(
            api_key=ANTHROPIC_API_KEY,
        )

    def _extract_prompt(
        self,
        history: List[Dict[str, str]]
    ) -> ExtractedPrompt:
        prompt = history[0]
        messages = history[1:]

        return self.ExtractedPrompt(
            prompt=prompt['content'],
            messages=messages
        )

    async def _get_response(
        self,
        prompt: str,
        history: List[Dict[str, str]]
    ) -> str:
        try:
            response: anthropic.types.Message = await self._client.messages.create(
                messages=history,
                model=MODEL,
                max_tokens=1024,
                system=prompt,
                tools=[
                    {
                        "type": "web_search_20260209",
                        "name": "web_search",
                        "max_uses": 5
                    }
                ],
                stream=False
            )

            text = "".join(
                block.text for block in response.content if block.type == "text"
            )
            return text
        except anthropic.APIError as e:
            logger.error(f"Could not get response from claude")
            raise RuntimeError(f"Could not get response from claude") from e

    async def run(
            self,
            history: List[Dict[str, str]]
        ) -> str:
            prompt_n_hisotry = self._extract_prompt(history)
            response = await self._get_response(
                prompt_n_hisotry.prompt, 
                prompt_n_hisotry.messages
            )
            return response