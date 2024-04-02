from app.core.conf import settings
from app.services.ml.faceMl import find_faces
from app.logger import logger
from pydantic import BaseModel, Field
from celery import Celery
import requests
import json

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
def predict_photo(photo: bytes) -> Prediction | None:
    """
    Predicting emotions in a photo using Tensorflow Serving deployed in Docker
    :param photo: photo data
    :return Prediction: Prediction class
    """
    faces = find_faces(photo)
    if faces is None:
        return None
    data = json.dumps({"signature_name": "serving_default", "instances": faces[0]})
    logger.info(f"Отправлен запрос к TF Serving")
    try:
        json_response = requests.post(url, data=data, headers=headers)
    except requests.exceptions.Timeout:
        logger.error("Timeout запроса к TF Serving")
    except requests.exceptions.ConnectionError:
        logger.error("ConnectionError запроса к TF Serving")
    predictions = json.loads(json_response.text)['predictions']
    return Prediction(happy=1, sad=1, normal=1, angry=1)
