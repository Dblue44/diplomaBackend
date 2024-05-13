from typing import List
from pydantic import BaseModel
from beanie import Document, PydanticObjectId
from beanie.operators import And

class Prediction(BaseModel):
    happy: float
    sad: float
    normal: float
    angry: float

class Music(BaseModel):
    id: PydanticObjectId
    artist: str
    trackName: str
    photoId: str


class musics(Document):
    artists: str
    track_name: str
    album_name: str
    popularity: int
    duration_ms: int
    explicit: bool
    danceability: float
    energy: float
    key: int
    loudness: float
    mode: int
    speechiness: float
    acousticness: float
    instrumentalness: float
    liveness: float
    valence: float
    tempo: float
    time_signature: int
    track_genre: str
    photoId: str


async def find_music(prediction: Prediction) -> List[Music] | None:
    """
    Search for music by a given distribution of emotions
    :param prediction:
    :return:
    """
    filters = _get_filters(prediction)
    musicData: list = await musics.find(filters).to_list()
    return [Music(id=music.id, artist=music.artists, trackName=music.track_name, photoId=music.photoId) for music in musicData]


def _get_filters(prediction: Prediction) -> And:
    ms = [prediction.happy, prediction.sad, prediction.normal, prediction.angry]
    max_index = ms.index(max(ms))
    match max_index:
        case 0:
            return And(musics.danceability > 0.8,
                   musics.valence > 0.8,
                   musics.tempo > 140,
                   musics.mode == 1)
        case 1:
            return And(musics.danceability < 0.3,
                   musics.valence > 0.4,
                   musics.valence < 0.6,
                   musics.tempo > 100,
                   musics.mode == 0)
        case 2:
            return And(musics.danceability > 0.4,
                   musics.danceability < 0.6,
                   musics.valence > 0.4,
                   musics.valence < 0.5,
                   musics.tempo < 100,
                   musics.mode == 0)
        case 3:
            return And(musics.danceability < 0.2,
                   musics.valence < 0.2,
                   musics.tempo > 140,
                   musics.mode == 0)
