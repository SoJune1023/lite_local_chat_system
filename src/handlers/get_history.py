from typing import Optional, List, Dict

from src.schemas.router import GetHistoryRequest, GetHistoryResponse
from src.services.history_loader import HistoryLoader

class GetHistory:
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
        data: GetHistoryRequest
    ) -> GetHistoryResponse:
        history = cls._load_history(data.max_messages)

        return GetHistoryResponse(
            messages=history
        )