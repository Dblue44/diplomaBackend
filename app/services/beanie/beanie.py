from typing import List
from app.services.celery.celery import Prediction
from app.services.graphql.mutation import Music
from beanie import Document
from beanie.operators import And


class MusicDoc(Document):
    musicId: str
    artist: str
    trackName: str
    photoId: str
    happy: float
    sad: float
    normal: float
    angry: float


def find_music(prediction: Prediction) -> List[Music] | None:
    musics: list = await MusicDoc.find(_get_filters(prediction)).to_list()
    return


def _get_filters(prediction: Prediction) -> And:
    _happy = And(MusicDoc.happy > prediction.happy - 0.1,
                 MusicDoc.happy < prediction.happy + 0.1)
    _sad = And(MusicDoc.sad > prediction.sad - 0.1,
               MusicDoc.sad < prediction.sad + 0.1)
    _normal = And(MusicDoc.normal > prediction.normal - 0.1,
                  MusicDoc.normal < prediction.normal + 0.1)
    _angry = And(MusicDoc.angry > prediction.angry - 0.1,
                 MusicDoc.angry < prediction.angry + 0.1)
    return And(_happy, _sad, _normal, _angry)
