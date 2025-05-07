from fastapi import FastAPI
from fastapi.exceptions import ResponseValidationError

from src.exceptions.handlers import (
    gateway_exception_handler,
    not_found_exception_handler,
    response_validation_exception_handler,
)
from src.exceptions.exceptions import GatewayRouterException, NotFoundException


def exception_container(app: FastAPI) -> None:
    app.add_exception_handler(GatewayRouterException, gateway_exception_handler)
    app.add_exception_handler(NotFoundException, not_found_exception_handler)
    app.add_exception_handler(
        ResponseValidationError, response_validation_exception_handler
    )
