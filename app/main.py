import uvicorn
from path import Path
from app.logger import logger
from app.core import settings, register_app

app = register_app()

if __name__ == '__main__':
    try:
        logger.info("Запуск FastAPI")
        uvicorn.run(
            app=f'{Path(__file__).stem}:app',
            host=settings.UVICORN_HOST,
            port=settings.UVICORN_PORT,
            reload=settings.UVICORN_RELOAD,
        )
    except Exception as e:
        logger.error(f'FastAPI завершился с ошибкой {e}')
