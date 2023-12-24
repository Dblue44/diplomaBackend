import strawberry
from fastapi import FastAPI

from .conf import settings
from app.api.routers import v1
from app.utils.health_check import ensure_unique_route_names
from app.utils.openapi import simplify_operation_ids
from strawberry.fastapi import GraphQLRouter
from strawberry.schema.config import StrawberryConfig
from app.services.graphql.query import Query
from app.services.graphql.mutation import Mutation

def register_app():
    # FastAPI
    app = FastAPI(
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

    # Exceptions
    # register_exception(app)

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
    # GraphQL
    schema = strawberry.Schema(query=Query, config=StrawberryConfig(auto_camel_case=True),)
    graphql_app = GraphQLRouter(schema)
    app.include_router(graphql_app, prefix='/graphql')

    # API
    app.include_router(v1)

    # Extra
    ensure_unique_route_names(app)
    simplify_operation_ids(app)
