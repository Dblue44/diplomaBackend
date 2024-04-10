from app.logger import logger
from app.core import settings
from app.services import find_faces
from pydantic import BaseModel, Field
from celery import Celery
import requests
import json

celery = Celery("app")
celery.conf.broker_url = settings.CELERY_BROKER_URL
celery.conf.result_backend = settings.CELERY_RESULT_BACKEND
celery.include = [
    "app.tasks"
]


class Prediction(BaseModel):
    happy: float = Field(default=1.0)
    sad: float = Field(default=1.0)
    normal: float = Field(default=1.0)
    angry: float = Field(default=1.0)


@celery.task(name="predict_photo")
def predict_photo(photo: str) -> Prediction | str:
    """
    Predicting emotions in a photo using Tensorflow Serving deployed in docker
    :param photo: photo data
    :return Prediction: Prediction class
    """
    faces = find_faces(photo)
    if faces is None:
        return "Нет лиц на фотографии"
    data = json.dumps({"signature_name": "serving_default", "instances": faces[0]})
    logger.info(f"Отправлен запрос к TF Serving")
    try:
        json_response = requests.post(settings.TF_URL, data=data, headers={"content-type": "application/json"})
    except requests.exceptions.Timeout:
        logger.error("Timeout запроса к TF Serving")
        return "Ошибка подключения к TF Serving."
    except requests.exceptions.ConnectionError:
        logger.error("ConnectionError запроса к TF Serving")
        return "Неправильный запрос к TF Serving"
    predictions = json.loads(json_response.text)['predictions']
    return Prediction(happy=1, sad=1, normal=1, angry=1)
