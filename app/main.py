from typing import Optional
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from dependency_injector.wiring import Provide, inject

from app.core.config import settings, TEST_MODE
from app.core.container import Container
from app.api.v1 import routers
from app.db import db_manager


@asynccontextmanager
@inject
async def lifespan(
    fastapi_app: FastAPI,
):

    yield

    await db_manager.dispose()


def create_app() -> FastAPI:
    fastapi_app = FastAPI(
        title=settings.project_name,
        default_response_class=ORJSONResponse,
        lifespan=lifespan,
    )
    container = Container()
    if not TEST_MODE:
        container.init_recources()
        
    container.wire(modules=settings.container_wiring_modules)

    fastapi_app.container = container
    fastapi_app.include_router(
        routers.api_router,
        prefix=settings.api_v1_prefix
    )

    return fastapi_app


app = create_app()


