import datetime

from pydantic import BaseModel, Field

from core.models.category import CategoryTypeEnum


class OperationSchema(BaseModel):
    budget_id: int = Field(ge=0)
    type_: CategoryTypeEnum
    value: int = Field(ge=0)
    description: str | None = None
    category_id: int = Field(ge=0)
    sub_category_id: int | None = None



class OperationResponseSchema(OperationSchema):
    id: int = Field(ge=0)
    date: datetime.datetime