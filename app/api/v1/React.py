from fastapi import APIRouter
from app.logger import logger

react_app = APIRouter()


@logger.catch
@react_app.post("/photo")
async def get_photo(fileId: str):
    #result = model.predict(file.read())
    return "123"
