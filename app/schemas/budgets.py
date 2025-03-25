import datetime

from pydantic import BaseModel, Field


class BudgetSchema(BaseModel):
    name: str
    user_id: int = Field(ge=0)
    currency_id: int = Field(ge=0)


class BudgetResponseSchema(BudgetSchema):
    id: int
    created: datetime.datetime
