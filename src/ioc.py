from dishka import Provider, provide, Scope, make_async_container

from src.application.mediator.bootstrap import init_mediator
from src.application.mediator.mediator import Mediator


class MediatorProvider(Provider):
    @provide(scope=Scope.APP)
    def init_mediator(self) -> Mediator:
        return init_mediator()


container = make_async_container(
    MediatorProvider(),
)
