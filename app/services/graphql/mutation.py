import strawberry
from strawberry.file_uploads import Upload
from typing import List
from app.services.beanie.beanie import find_music
from app.services.celery.celery import predict_photo


@strawberry.type
class Prediction:
    happy: float
    sad: float
    normal: float
    angry: float


@strawberry.type
class Music:
    id: str
    artist: str
    trackName: str
    photoId: str


@strawberry.type
class Predict:
    prediction: Prediction
    music: List[Music]


@strawberry.type
class Mutation:
    @strawberry.mutation
    async def photoUpload(self, file: Upload) -> Predict:
        fileData: bytes = await file.read()
        photoPredictionTask = predict_photo.delay(fileData)
        photoPrediction = photoPredictionTask.get()
        # music = [Music(id="11", artist="artist1", trackName="track1", photoId="file_png"),
        #          Music(id="12", artist="artist2", trackName="track2", photoId="file_png"),
        #          Music(id="13", artist="artist3", trackName="track3", photoId="file_png"),
        #          Music(id="14", artist="artist4", trackName="track4", photoId="file_png")]
        music = find_music(photoPrediction)
        predictRes = Predict(prediction=photoPrediction, music=music)
        return predictRes

