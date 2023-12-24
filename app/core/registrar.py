from fastapi import FastAPI
from fastapi_pagination import add_pagination
from .conf import settings
from app.api.routers import v1
from app.utils.health_check import ensure_unique_route_names
from app.utils.openapi import simplify_operation_ids


def register_app():
    # FastAPI
    app = FastAPI(
        title=settings.TITLE,
        version=settings.VERSION,
        description=settings.DESCRIPTION,
        docs_url=settings.DOCS_URL,
        redoc_url=settings.REDOCS_URL,
        openapi_url=settings.OPENAPI_URL,
        # lifespan=register_init, - REDIS
    )

    # Middlewares
    register_middleware(app)

    # Routers
    register_router(app)

    # Pagination
    register_page(app)

    # Exceptions
    # register_exception(app)

    return app


def register_middleware(app: FastAPI):
    """
    Add Middewares, the execution order is from bottom to top

    :param app:
    :return:
    """
    # Gzip: Always at the top
    if settings.MIDDLEWARE_GZIP:
        from fastapi.middleware.gzip import GZipMiddleware

        app.add_middleware(GZipMiddleware)
    # Access log
    if settings.MIDDLEWARE_ACCESS:
        from app.middlewares.access_middleware import AccessMiddleware

        app.add_middleware(AccessMiddleware)
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


def register_page(app: FastAPI):
    """
    Paging query

    :param app:
    :return:
    """
    add_pagination(app)
