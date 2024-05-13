import io
from typing import List, Annotated
from fastapi import APIRouter, Response, HTTPException, File, status
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from app.logger import logger
from app.services import get_photo_from_aws, get_music_from_aws, find_music, Music
from app.tasks import predict_photo, Prediction

react_app = APIRouter()


class Predict(BaseModel):
    prediction: Prediction
    music: List[Music]


@logger.catch
@react_app.get("/photo")
async def get_photo(fileId: str) -> Response:
    bytesData = await get_photo_from_aws(fileId)
    if bytesData:
        return Response(content=bytesData, media_type="image/avif,image/webp,image/apng,image/svg+xml,image/png")
    else:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Photo not found")


@logger.catch
@react_app.get("/music")
async def get_music(musicId: str) -> Response:
    bytesData = await get_music_from_aws(musicId)
    if bytesData:
        return StreamingResponse(
            status_code=status.HTTP_200_OK,
            content=io.BytesIO(bytesData),
            media_type="application/octet-stream",
            headers={"Content-Disposition": f"attachment; filename={musicId}"}
        )
    else:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Music not found")


@logger.catch
@react_app.post("/uploadPhoto")
async def upload_photo(file: Annotated[bytes, File()]) -> None:
    logger.info(f"Получено фото")
    photoPredictionResult = await predict_photo(file)
    if type(photoPredictionResult) is str:
        logger.warning(f"Получена ошибка: {photoPredictionResult}")
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail=photoPredictionResult)
    music = await find_music(photoPredictionResult)
    return Predict(prediction=photoPredictionResult, music=music)
