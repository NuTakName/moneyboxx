import datetime

from pydantic import BaseModel, Field


class MoneyboxSchema(BaseModel):
    user_id: int = Field(ge=0)
    name: str
    currency_id: int = Field(ge=0)
    current_balance: int
    goal_balance: int
    goal_date: datetime.date


class MoneyboxResponseSchema(MoneyboxSchema):
    is_finished: bool = False
    created: datetime.datetime
    id: int = Field(ge=0)