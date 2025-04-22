from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from src.application.exceptions.mediator import MediatorException
from src.domain.exceptions.base import ApplicationException


def register_exceptions_handlers(app: FastAPI) -> None:
    @app.exception_handler(MediatorException)
    def mediator_exception_handler(
            request: Request,
            exc: MediatorException,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "detail": exc.message,
            }
        )

    @app.exception_handler(ApplicationException)
    def application_exception_handler(
            request: Request,
            exc: ApplicationException,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "detail": exc.message,
            }
        )
