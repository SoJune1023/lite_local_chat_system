from fastapi import APIRouter, status

from src.schemas.router import GetHistoryRequest, GetHistoryResponse
from src.handlers.get_history import GetHistory

router = APIRouter(
    prefix="/get_history",
    tags=["get_history"]
)

@router.get("", status_code=status.HTTP_200_OK)
async def interaction(data: GetHistoryRequest) -> GetHistoryResponse:
    res = await GetHistory().process(data)
    return res