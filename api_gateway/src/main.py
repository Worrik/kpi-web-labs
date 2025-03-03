from fastapi import FastAPI

from src.routers import generic
from src.exceptions.container import exception_container


def get_app() -> FastAPI:
    app = FastAPI()
    app.include_router(generic.router)
    exception_container(app)
    return app
