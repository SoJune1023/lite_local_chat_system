from typing import Optional, List, Dict

from src.schemas.router import GetHistoryResponse
from src.services.history_loader import HistoryLoader

class GetHistoryHandler:
    @classmethod
    def _load_history(
        cls,
        max_messages: int
    ) -> Optional[List[Dict[str, str]]]:
        loader = HistoryLoader()
        history = loader.run(max_messages)
        return history

    async def process(
        cls,
        max_messages: int
    ) -> GetHistoryResponse:
        history = cls._load_history(max_messages)

        return GetHistoryResponse(
            messages=history.history
        )