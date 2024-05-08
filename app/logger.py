from loguru import logger

logger.add("/etc/logs/debug.log", format="{time} {level} {message}",
           level="DEBUG", rotation="01:00", compression="zip", serialize=True)

