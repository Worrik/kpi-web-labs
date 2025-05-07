from fastapi import Request, status
from fastapi.exceptions import ResponseValidationError
from fastapi.responses import JSONResponse, Response


async def gateway_exception_handler(request: Request, exc: Exception) -> Response:
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST, content={"detail": str(exc)}
    )


async def not_found_exception_handler(request: Request, exc: Exception) -> Response:
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND, content={"detail": str(exc)}
    )


async def forbidden_exception_handler(request: Request, exc: Exception) -> Response:
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN, content={"detail": str(exc)}
    )


async def response_validation_exception_handler(
    request: Request, exc: Exception
) -> Response:
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=(
            exc.body
            if isinstance(exc, ResponseValidationError)
            else {"detail": str(exc)}
        ),
    )
