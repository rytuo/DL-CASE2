import logging
from contextlib import asynccontextmanager
from functools import partial

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.api_v1.api import router
from core.settings import settings
from middlewares.exception import json_exceptions_wrapper_middleware
from services.model import ModelService

logger = logging.getLogger("API")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Loading models started")
    model_service = ModelService()
    app.state.model_service = model_service
    logger.info("Loading models ended")
    yield
    app.state.model_service = None


app = FastAPI(title="Anima API Gateway", description="API Gateway для сервисов Anima", lifespan=lifespan)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS,
)
app.middleware("http")(partial(json_exceptions_wrapper_middleware))

app.include_router(router, prefix="/api/v1")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
