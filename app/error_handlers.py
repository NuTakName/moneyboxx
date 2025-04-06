from traceback import format_exc

from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import ORJSONResponse
from loguru import logger
from starlette import status
from starlette.requests import Request



async def validation_exception_handler(
    request: Request, exception: RequestValidationError
):
    text = (
        f"client ip: {request.client.host} ({request.client.host})\n"
        f"{request.url}"
        f"\n{format_exc()[-3000:]}"
        f"\n{exception.errors()}"
    )
    logger.error(text)
    content = jsonable_encoder(
        {"status_code": 422, "message": exception.body, "data": exception.errors()}
    )
    return ORJSONResponse(
        content=content, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
    )


async def internal_exception_handler(request: Request, exc: Exception):
    text = (
        f"Client ip: {request.client.host} ({request.client.host})\n"
        f"{request.url}\n"
        f"{format_exc()[-3000:]}"
    )
    logger.error(text)
    return ORJSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=jsonable_encoder({"code": 500, "msg": "Internal Server Error"}),
    )