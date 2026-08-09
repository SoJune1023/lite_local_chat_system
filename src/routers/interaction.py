from fastapi import APIRouter, status

from src.schemas.router import (
    InteractionRequest, InteractionResponse,
    GetHistoryResponse
)
from src.handlers.interaction import InteractionHandler
from src.handlers.get_history import GetHistoryHandler

router = APIRouter(
    prefix="/interaction",
    tags=["interaction"]
)

@router.post("", status_code=status.HTTP_200_OK)
async def interaction(data: InteractionRequest) -> InteractionResponse:
    res = await InteractionHandler().process(data)
    return res

@router.get("/history", status_code=status.HTTP_200_OK)
async def get_history(max_messages: int) -> GetHistoryResponse:
    res = await GetHistoryHandler().process(max_messages)
    return res