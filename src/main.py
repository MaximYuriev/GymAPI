from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from src.ioc.ioc import container
from src.presentation.api.handlers.customer import customer_router
from src.presentation.api.handlers.ticket import ticket_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="GymAPI",
        description="API для тренажерного зала",
        debug=True,
    )

    app.include_router(ticket_router)
    app.include_router(customer_router)

    setup_dishka(container, app)

    return app
