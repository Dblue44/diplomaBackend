import os
from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Uvicorn
    UVICORN_HOST: str = '127.0.0.1'
    UVICORN_PORT: int = 80
    UVICORN_RELOAD: bool = True

    # FastAPI
    API_V1_STR: str = '/api/v1'
    TITLE: str = 'FastAPI'
    VERSION: str = '0.0.1'
    DESCRIPTION: str = 'FastAPITelegramBot'
    DOCS_URL: str | None = f'{API_V1_STR}/docs'
    REDOCS_URL: str | None = f'{API_V1_STR}/redocs'
    OPENAPI_URL: str | None = f'{API_V1_STR}/openapi'

    # AWS
    AWS_ACCESS_KEY_ID: str = os.environ['AWS_ACCESS_KEY_ID']
    AWS_SECRET_ACCESS_KEY: str = os.environ['AWS_SECRET_ACCESS_KEY']
    AWS_S3_BUCKET_NAME: str = os.environ['AWS_S3_BUCKET_NAME']
    AWS_S3_ENDPOINT_URL: str = os.environ['AWS_S3_ENDPOINT_URL']
    AWS_DEFAULT_REGION: str = os.environ['AWS_DEFAULT_REGION']

    # MongoDB
    MONGO_HOST: str = 'localhost'  # mongodb
    MONGO_PORT: int = 28017
    MONGO_USER: str = os.environ['MONGO_USER']
    MONGO_PASS: str = os.environ['MONGO_PASS']
    MONGO_URL: str = f'mongodb://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOST}:{MONGO_PORT}'

    # Tensorflow
    TF_HOST: str = 'localhost'  # tf-serving
    TF_PORT: int = 8500
    TF_VERSION: str = 'v1'
    TF_URL: str = f"http://{TF_HOST}:{TF_PORT}/{TF_VERSION}/models/e-motion_detector:predict"

    # Middleware
    MIDDLEWARE_CORS: bool = True


@lru_cache
def get_settings():
    return Settings()


settings = get_settings()
