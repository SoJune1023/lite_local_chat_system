from fastapi import APIRouter, status, Depends

from src.schemas.router import InteractionRequest, InteractionResponse
from src.handlers.interaction import InteractionHandler

router = APIRouter(
    prefix="/interaction",
    tags=["interaction"]
)

@router.post("", status_code=status.HTTP_200_OK)
async def interaction(data: InteractionRequest) -> InteractionResponse:
    res = await InteractionHandler().process(data)
    return res