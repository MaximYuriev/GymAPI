from dataclasses import dataclass

from src.domain.exceptions.base import ApplicationException


@dataclass(frozen=True, eq=False)
class TicketTypeAlreadyExistException(ApplicationException):
    type_name: str

    @property
    def message(self) -> str:
        return f"Тип абонемента с таким названием: '{self.type_name}' уже существует!"
