from uuid import UUID, uuid4
from pydantic import Field
from beanie import Document


class Prediction(Document):
    happy: float
    sad: float
    normal: float
    angry: float


class Music(Document):
    id: UUID = Field(default_factory=uuid4)
    artist: str
    trackName: str
    photoId: UUID = Field(default_factory=uuid4)



