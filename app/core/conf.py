import os
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Uvicorn
    UVICORN_HOST: str = '127.0.0.1'
    UVICORN_PORT: int = 8000
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

    # Redis
    REDIS_HOST: str = 'localhost'
    REDIS_PORT: int = 6379
    REDIS_DB: str = '0'

    # MongoDB
    MONGO_HOST: str = 'localhost'
    MONGO_PORT: int = 27017
    MONGO_URL: str = f'mongodb://{MONGO_HOST}:{MONGO_PORT}'

    # Tensorflow
    TF_HOST: str = 'localhost'
    TF_PORT: int = 8025
    TF_VERSION: str = 'v1'

    # Middleware
    MIDDLEWARE_CORS: bool = True

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')


@lru_cache
def get_settings():
    return Settings()


settings = get_settings()
