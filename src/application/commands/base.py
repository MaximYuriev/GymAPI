from abc import ABC
from dataclasses import dataclass


@dataclass(frozen=True, eq=False)
class BaseCommand(ABC):
    pass
