from celery import Celery
from app.core.conf import settings
import requests
import json

celery = Celery()
celery.conf.broker_url = f'redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_DB}'
celery.conf.result_backend = f'redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_DB}'


@celery.task(name="predict_photo")
async def predict_photo(data: list):
    url = f"http://{settings.TF_HOST}:{settings.TF_PORT}/{settings.TF_VERSION}/models/e-motion_detector:predict"
    data = json.dumps({"signature_name": "serving_default", "instances": data})
    headers = {"content-type": "application/json"}
    json_response = requests.post(url, data=data, headers=headers)
    predictions = json.loads(json_response.text)['predictions']
    return predictions
