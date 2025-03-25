from pydantic import BaseModel, Field

from core.models.currency import CurrencyTypeEnum


class CurrencySchema(BaseModel):
    name: str
    code: str
    type_: CurrencyTypeEnum
    symbol: str | None = None


class CurrencyResponseSchema(CurrencySchema):
    id: int = Field(ge=0)