import sys

import uvicorn
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from loguru import logger
from notifiers.logging import NotificationHandler
from starlette.middleware.cors import CORSMiddleware

from app.error_handlers import validation_exception_handler, internal_exception_handler
from app.routers import users, budgets, currency, categories, operations, moneybox
from config import settings

app = FastAPI()

logger.add(
    sys.stdout,
    colorize=True,
    format="<green>{time:HH:mm:ss}</green> | {level} | <level>{message}</level>",
)

params = {
    "token": settings["logger"]['logger_telegram_token'],
    "chat_id": settings["logger"]['logger_telegram_chat_id'],
}

handler = NotificationHandler("telegram", defaults=params)
logger.add(handler, level="ERROR", backtrace=True)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(500, internal_exception_handler)

app.include_router(users.router)
app.include_router(budgets.router)
app.include_router(currency.router)
app.include_router(categories.router)
app.include_router(operations.router)
app.include_router(moneybox.router)



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == "__main__":
    uvicorn.run(
        "server:app",
        host="0.0.0.0",
        port=9999,
        workers=1,
    )