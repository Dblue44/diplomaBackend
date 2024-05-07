from app.logger import logger
from app.core import settings
from app.services import find_faces
from pydantic import BaseModel
import requests
import json


class Prediction(BaseModel):
    happy: float
    sad: float
    normal: float
    angry: float


@logger.catch
async def predict_photo(photo: bytes) -> Prediction | str:
    """
    Predicting emotions in a photo using Tensorflow Serving deployed in docker
    :param photo: photo data
    :return Prediction: Prediction class
    """
    faces = find_faces(photo)
    if faces is None:
        return "Нет лиц на фотографии"
    data = json.dumps({"signature_name": "serving_default", "instances": faces[0]})
    try:
        json_response = requests.post(settings.TF_URL, data=data, headers={"content-type": "application/json"})
        logger.info(f"Ответ от TF Serving: {json.loads(json_response.text)}")
    except requests.exceptions.Timeout:
        logger.error("Timeout запроса к TF Serving")
        return "Ошибка подключения к TF Serving."
    except requests.exceptions.ConnectionError:
        logger.error("ConnectionError запроса к TF Serving")
        return "Неправильный запрос к TF Serving"
    predictions = json.loads(json_response.text)['predictions']
    return Prediction(happy=1, sad=1, normal=1, angry=1)
