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
        fileData = await file.read()
        predict = Prediction(happy=1, sad=1, normal=1, angry=1)
        music = [Music(id="1", artist="artist1", trackName="track1", photoId="photo1"),
                 Music(id="2", artist="artist2", trackName="track2", photoId="photo2"),
                 Music(id="3", artist="artist3", trackName="track3", photoId="photo3"),
                 Music(id="4", artist="artist4", trackName="track4", photoId="photo4")]
        predictRes = Predict(prediction=predict, music=music)
        return predictRes

    @strawberry.mutation
    async def photoUpload2(self) -> Predict:
        predict = Prediction(happy=1, sad=1, normal=1, angry=1)
        music = [Music(id="1", artist="artist1", trackName="track1", photoId="photo1"),
                 Music(id="2", artist="artist2", trackName="track2", photoId="photo2"),
                 Music(id="3", artist="artist3", trackName="track3", photoId="photo3"),
                 Music(id="4", artist="artist4", trackName="track4", photoId="photo4")]
        predictRes = Predict(prediction=predict, music=music)
        return predictRes

