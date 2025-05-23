import datetime

from pydantic import BaseModel, Field

from app.schemas.currency import CurrencyResponseSchema
from core.models.category import CategoryTypeEnum

class BaseOperationSchema(BaseModel):
    budget_id: int = Field(ge=0)
    type_: CategoryTypeEnum
    value: int = Field(ge=0)
    description: str | None = None
    category_id: int = Field(ge=0)
    sub_category_id: int | None = None


class OperationSchema(BaseOperationSchema):
    date: datetime.datetime


class UpdateOperationSchema(BaseOperationSchema):
    id: int = Field(ge=0)


class OperationResponseSchema(OperationSchema):
    id: int = Field(ge=0)
    date: datetime.datetime

class OperationAndCategoryResponseSchema(OperationResponseSchema):
    category_name: str
    currency_code: str
    currency_symbol: str | None = None

class OperationTotalAmountSchema(BaseModel):
    total_amount_income: int
    total_amount_expense: int

class DifferenceResponseSchema(BaseModel):
    difference: int


class StatisticResponseSchema(OperationTotalAmountSchema):
    count_moneybox: int
    currency: CurrencyResponseSchema

class StatisticSchema(BaseModel):
    user_id: int = Field(ge=0)
    month: int | None = None
    year: int | None = None

class OperationStatisticResponseSchema(OperationResponseSchema):
    category_name: str
    currency: CurrencyResponseSchema