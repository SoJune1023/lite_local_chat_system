import os
import json
import logging

from typing import Literal, Optional

from src.schemas.context import History

HISTORY_PATH = os.getenv('HISTORY_PATH')

logger = logging.getLogger(__name__)

class HistoryLoader:
    history: Optional[History]

    def __init__(self):
        self.history = None

    def _read_file(
        self,
        max_messages: int
    ) -> None:
        try:
            with open(HISTORY_PATH, 'r', encoding='utf-8') as f:
                content = f.read().strip()

            if not content:
                self.history = History(history=[])
            else:
                data = json.loads(content)
                history_obj = History(history=[]) if not data else History.model_validate(data)
                self.history = History(history=history_obj.history[-max_messages:])
        except FileNotFoundError as e:
            logger.error(f"Could not found history. History path : {HISTORY_PATH}")
            raise e

    def run(
        self,
        max_messages: int = 12
    ) -> History:
        self._read_file(max_messages)
        return self.history