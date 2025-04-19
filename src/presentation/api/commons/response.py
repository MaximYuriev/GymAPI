from pydantic import BaseModel


class APIResponse[T: BaseModel](BaseModel):
    detail: str
    data: T | list[T] | None = None
