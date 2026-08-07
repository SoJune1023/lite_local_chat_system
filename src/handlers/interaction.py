from typing import Literal, Dict, List

from src.schemas.router import InteractionRequest, InteractionResponse
from src.schemas.context import History
from src.services.prompt_loader import PromptLoader
from src.services.history_loader import HistoryLoader
from src.services.response_maker import ResponseMaker
from src.services.history_saver import HistorySaver

class InteractionHandler:
    @classmethod
    def _load_prompt(cls) -> str:
        loader = PromptLoader()
        prompt = loader.run()
        return prompt

    @classmethod
    def _load_history(cls) -> History:
        loader = HistoryLoader()
        history = loader.run()
        return history

    @classmethod
    def _make_prompt(
        cls,
        history: History,
        user_message: str,
        prompt: str
    ) -> List[Dict[str, str]]:
        prompt_dict = {
            "role": "system",
            "content": prompt
        }

        user_message_dict = {
            "role": "user",
            "content": user_message
        }
        
        messages = []

        messages.append(prompt_dict)
        messages.extend(history.history)
        messages.append(user_message_dict)

        return messages

    @classmethod
    async def _make_response(
        cls,
        history: List[Dict[str, str]]
    ) -> str:
        maker = ResponseMaker()
        response = await maker.run(history)
        return response

    @classmethod
    def _save_data(
        cls,
        user_message: str,
        system_message: str
    ) -> Literal[True]:
        saver = HistorySaver()
        saver.run(user_message, system_message)

        return True

    async def process(
        cls,
        data: InteractionRequest
    ) -> InteractionResponse:
        prompt = cls._load_prompt()
        history = cls._load_history()
        full_history = cls._make_prompt(history, data.message, prompt)

        response = await cls._make_response(full_history)

        cls._save_data(data.message, response)

        return InteractionResponse(
            message=response
        )