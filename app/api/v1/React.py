from fastapi import APIRouter, Response, HTTPException
from app.logger import logger
from app.services.aws.aws import get_photo_from_aws, get_music_from_aws

react_app = APIRouter()


@logger.catch
@react_app.get("/photo")
async def get_photo(fileId: str) -> Response:
    bytesData = await get_photo_from_aws(fileId)
    if bytesData:
        return Response(content=bytesData, media_type="image/avif,image/webp,image/apng,image/svg+xml,image/png")
    else:
        HTTPException(status_code=204, detail="Photo not found")


@logger.catch
@react_app.get("/music")
async def get_music(musicId: str) -> Response:
    bytesData = await get_music_from_aws(musicId)
    if bytesData:
        return Response(content=bytesData, media_type="audio/mpeg")
    else:
        HTTPException(status_code=204, detail="Music not found")
