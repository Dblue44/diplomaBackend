# from uuid import UUID, uuid4
# from pydantic import Field
from typing import List
from app.services.celery.celery import Prediction
from app.services.graphql.mutation import Music
from beanie import Document


class MusicDoc(Document):
    artist: str
    trackName: str
    photoId: str
    musicId: str


def find_music(prediction: Prediction) -> List[Music]:
    pass
