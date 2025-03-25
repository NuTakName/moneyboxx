from enum import StrEnum, auto
from core.base import BaseModel
from core.async_session import async_session

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Enum, select


class CurrencyTypeEnum(StrEnum):
    fiat = auto()
    crypto = auto()


class Currency(BaseModel):

    __tablename__ = "currencies"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(180), nullable=False)
    code: Mapped[str] = mapped_column(String(180), nullable=False)
    type_: Mapped[CurrencyTypeEnum] = mapped_column(
        Enum(CurrencyTypeEnum, name="currency_type_enum"),
        nullable=False,
        index=True
    )
    symbol: Mapped[str] = mapped_column(String(10), nullable=True)


    @staticmethod
    async def get_by_name(name: str) -> "Currency":
        async with async_session() as session:
            result = await session.execute(
                select(Currency).where(Currency.name.ilike(name))
            )
            return result.scalars().first()
