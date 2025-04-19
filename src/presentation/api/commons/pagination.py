from pydantic import BaseModel, Field


class PaginationQueryParams(BaseModel):
    limit: int = Field(default=5, gt=0)
    offset: int = Field(default=0, ge=0)
