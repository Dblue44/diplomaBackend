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
    def photoUpload(self, file: Upload) -> Predict:
        fileData: bytes = await file.read()
        photoPredictionTask = predict_photo.delay(fileData)
        photoPrediction = photoPredictionTask.get()
        music = find_music(photoPrediction)
        return Predict(prediction=photoPrediction, music=music)
