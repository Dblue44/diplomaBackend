import typing
from contextlib import asynccontextmanager
from fastapi import FastAPI
# from motor.motor_asyncio import AsyncIOMotorClient
# from beanie import init_beanie
# from app.services import MusicDoc
from app.core import settings
from app.api import v1
from app.utils import ensure_unique_route_names, simplify_operation_ids


@asynccontextmanager
async def lifespan(application: FastAPI) -> typing.AsyncGenerator[None, None]:
    # logger.info("Start connection to MongoDB")
    # client = AsyncIOMotorClient(settings.MONGO_URL)
    # await init_beanie(database=client.db_name, document_models=[MusicDoc])
    # logger.info("MongoDB was connected successfully")
    yield


def register_app():
    # FastAPI
    app = FastAPI(
        lifespan=lifespan,
        title=settings.TITLE,
        version=settings.VERSION,
        description=settings.DESCRIPTION,
        docs_url=settings.DOCS_URL,
        redoc_url=settings.REDOCS_URL,
        openapi_url=settings.OPENAPI_URL,
    )

    # Middlewares
    register_middleware(app)

    # Routers
    register_router(app)

    return app


def register_middleware(app: FastAPI):
    """
    Add Middewares, the execution order is from bottom to top

    :param app:
    :return:
    """

    # CORS: Always at the end
    if settings.MIDDLEWARE_CORS:
        from fastapi.middleware.cors import CORSMiddleware
        app.add_middleware(
            CORSMiddleware,
            allow_origins=['*'],
            allow_credentials=True,
            allow_methods=['*'],
            allow_headers=['*'],
        )


def register_router(app: FastAPI):
    """
    Routing

    :param app: FastAPI
    :return:
    """

    # API
    app.include_router(v1)

    # Extra
    ensure_unique_route_names(app)
    simplify_operation_ids(app)
