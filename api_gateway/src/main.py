from fastapi import FastAPI
from dishka import make_async_container
from dishka.integrations import fastapi as fastapi_integration

from src.ioc import AppProvider
from src.config import Config
from src.routers import users, posts, images
from src.exceptions.container import exception_container


config = Config.parse()
container = make_async_container(
    AppProvider(),
    context={Config: config},
)


def get_app() -> FastAPI:
    app = FastAPI()
    app.include_router(users.router)
    app.include_router(posts.router)
    app.include_router(images.router)
    exception_container(app)
    fastapi_integration.setup_dishka(container, app)
    return app
