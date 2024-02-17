import uuid
import strawberry
from strawberry.file_uploads import Upload
from typing import List


@strawberry.type
class Prediction:
    happy: float
    sad: float
    normal: float
    angry: float


@strawberry.type
class Music:
    id: uuid
    artist: str
    trackName: str
    photoId: uuid


@strawberry.type
class Predict:
    prediction: Prediction
    music: List[Music]


@strawberry.type
class Mutation:
    @strawberry.mutation
    async def photoUpload(self, file: Upload) -> Predict:
        fileData = await file.read()
        print(type(fileData))
        return Predict()
