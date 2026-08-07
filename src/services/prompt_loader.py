import os
import logging

from pathlib import Path
from typing import Literal, Optional

PROMPT_PATH = os.getenv('PROMPT_PATH')

logger = logging.getLogger(__name__)

class PromptLoader:
    prompt: Optional[str]

    def __init__(self):
        self.prompt = None

    def _read_file(self) -> Literal[True]:
        try:
            with open(PROMPT_PATH, 'r', encoding='utf-8') as f:
                self.prompt = f.read().strip()
                
            return True
        except FileNotFoundError as e:
            logger.error(f"Could not found prompt. Prompt path : {PROMPT_PATH}")
            raise e

    def run(self) -> str:
        self._read_file()
        return self.prompt