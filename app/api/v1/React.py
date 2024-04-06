from typing import List, Annotated

from fastapi import APIRouter, Response, HTTPException, File
from pydantic import BaseModel

from app.logger import logger
from app.services.aws.aws import get_photo_from_aws, get_music_from_aws
from app.tasks import predict_photo

react_app = APIRouter()


class Prediction(BaseModel):
    happy: float
    sad: float
    normal: float
    angry: float


class Music(BaseModel):
    id: str
    artist: str
    trackName: str
    photoId: str


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
        raise HTTPException(status_code=204, detail="Photo not found")


@logger.catch
@react_app.get("/music")
async def get_music(musicId: str) -> Response:
    bytesData = await get_music_from_aws(musicId)
    if bytesData:
        return Response(content=bytesData, media_type="audio/mpeg")
    else:
        raise HTTPException(status_code=204, detail="Music not found")


@logger.catch
@react_app.post("/uploadPhoto")
async def upload_photo(file: Annotated[bytes, File()]) -> None:
    logger.info(f"Получено фото")
    photoPredictionTask = predict_photo.apply_async(args=[file], countdown=5)
    photoPrediction = photoPredictionTask.get()
    if photoPrediction is None:
        logger.warning("Лица на фотографии не найдены")
        raise HTTPException(status_code=204, detail="Лица на фотографии не найдены")
    # music = await find_music(photoPrediction)
    music1 = Music(id="1", artist="2", trackName="3", photoId="4")
    return Predict(prediction=photoPrediction, music=[music1])
