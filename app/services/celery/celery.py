from celery import Celery
from app.core.conf import settings
from pydantic import BaseModel, Field
import requests
import json

from app.services.ml.faceMl import find_faces

celery = Celery()
celery.conf.broker_url = f'redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_DB}'
celery.conf.result_backend = f'redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_DB}'
url = f"http://{settings.TF_HOST}:{settings.TF_PORT}/{settings.TF_VERSION}/models/e-motion_detector:predict"
headers = {"content-type": "application/json"}


class Prediction(BaseModel):
    happy: float = Field(default=1.0)
    sad: float = Field(default=1.0)
    normal: float = Field(default=1.0)
    angry: float = Field(default=1.0)


@celery.task(name="predict_photo")
def predict_photo(photo: bytes) -> Prediction:
    faces = find_faces(photo)
    data = json.dumps({"signature_name": "serving_default", "instances": faces[0]})
    json_response = requests.post(url, data=data, headers=headers)
    predictions = json.loads(json_response.text)['predictions']
    return Prediction(happy=1, sad=1, normal=1, angry=1)
