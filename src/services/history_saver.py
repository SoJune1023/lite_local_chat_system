import os
import json
import logging

from pathlib import Path
from typing import Literal, Optional, Dict, List

from src.schemas.context import History

HISTORY_PATH = os.getenv('HISTORY_PATH')

logger = logging.getLogger(__name__)

class HistorySaver:
    history: Optional[History]

    def __init__(self):
        self.history = None

    def _read_file(self) -> Literal[True]:
        try:
            with open(HISTORY_PATH, 'r', encoding='utf-8') as f:
                content = f.read().strip()

            if not content:
                self.history = History(history=[])
            else:
                data = json.loads(content)
                self.history = History(history=[]) if not data else History.model_validate(data)

            return True
        except FileNotFoundError as e:
            logger.error(f"Could not found history. History path : {HISTORY_PATH}")
            raise e

    def _append_history(
        self,
        user_message: str,
        system_message: str
    ) -> List[Dict[str, str]]:
        user_message_obj = {
            "role": "user",
            "content": user_message
        }
        system_message_obj = {
            "role": "assistant",
            "content": system_message
        }

        history_list = self.history.history

        history_list.append(user_message_obj)
        history_list.append(system_message_obj)

        return history_list

    def _save_file(
        self,
        history: List[Dict[str, str]]
    ) -> Literal[True]:
        try:
            with open(HISTORY_PATH, 'w', encoding='utf-8') as f:
                json.dump({"history": history}, f, ensure_ascii=False, indent=2)

            return True
        except FileNotFoundError as e:
            logger.error(f"Could not found history. History path : {HISTORY_PATH}")
            raise e

    def run(
        self,
        user_message: str,
        system_message: str
    ) -> Literal[True]:
        self._read_file()
        history = self._append_history(user_message, system_message)
        self._save_file(history)

        return True