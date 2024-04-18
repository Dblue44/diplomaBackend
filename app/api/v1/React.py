from typing import List, Annotated
from fastapi import APIRouter, Response, HTTPException, File, status
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from app.logger import logger
from app.services import get_photo_from_aws, get_music_from_aws, find_music
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
        return StreamingResponse(
            status_code=status.HTTP_200_OK,
            media_type="image/avif,image/webp,image/apng,image/svg+xml,image/png",
            content=bytesData,
            headers={"Content-Disposition": f"attachment; filename={fileId}"}
        )
        # return Response(content=bytesData, media_type="image/avif,image/webp,image/apng,image/svg+xml,image/png")
    else:
        raise HTTPException(status_code=204, detail="Photo not found")


@logger.catch
@react_app.get("/music")
async def get_music(musicId: str) -> Response:
    bytesData = await get_music_from_aws(musicId)
    if bytesData:
        return StreamingResponse(
            status_code=status.HTTP_200_OK,
            media_type="audio/mpeg",
            content=bytesData,
            headers={"Content-Disposition": f"attachment; filename={musicId}"}
        )
        # return Response(content=bytesData, media_type="audio/mpeg")
    else:
        raise HTTPException(status_code=204, detail="Music not found")


@logger.catch
@react_app.post("/uploadPhoto")
async def upload_photo(file: Annotated[bytes, File()]) -> None:
    logger.info(f"Получено фото")
    photoPredictionTask = predict_photo.apply_async(args=[file], countdown=10)
    photoPredictionResult: Prediction | str = photoPredictionTask.get()
    if type(photoPredictionResult) is str:
        logger.warning(f"Получена ошибка от Celery: {photoPredictionResult}")
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail=photoPredictionResult)
    # music = await find_music(photoPrediction)

    music1 = Music(id="1", artist="2", trackName="3", photoId="4")
    return Predict(prediction=photoPredictionResult, music=[music1])
