#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from ..logger import logger
from app.utils.timezone import timezone


class AccessMiddleware(BaseHTTPMiddleware):
    """Record request log middleware"""

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        start_time = timezone.now()
        response = await call_next(request)
        end_time = timezone.now()
        logger.info(
            f'{response.status_code} {request.client.host} {request.method} {request.url} {end_time - start_time}')
        return response
