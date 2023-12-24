#from app.services.graphql.query import Query
#from app.services.graphql.mutation import Mutation
import uvicorn
from path import Path
from app import logger
from app.core.conf import settings
from app.core.registrar import register_app
#from strawberry.fastapi import GraphQLRouter


app = register_app()
#schema = strawberry.Schema(query=Query, mutation=Mutation)
#graphql_app = GraphQLRouter(schema)

if __name__ == '__main__':
    try:
        logger.info("Start Telegram Bot")
        uvicorn.run(
            app=f'{Path(__file__).stem}:app',
            host=settings.UVICORN_HOST,
            port=settings.UVICORN_PORT,
            reload=settings.UVICORN_RELOAD,
        )
    except Exception as e:
        logger.error(f'FastAPI start filed: {e}')