from fastapi import APIRouter
from app.logger import logger

react_app = APIRouter()


@logger.catch
@react_app.post("/sendToTelegram")
async def send_to_telegram(request):

    return {"123"}
