import datetime
from typing import Union

from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, BIGINT, ForeignKey, Boolean, select


from core.base import BaseModel
from core.async_session import async_session
from core.models.currency import Currency



class MoneyBox(BaseModel):

    __tablename__ = "moneybox"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        BIGINT,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=True
    )
    name: Mapped[str] = mapped_column(String(180), nullable=False)
    currency_id: Mapped[str] = mapped_column(
        Integer,
        ForeignKey("currencies.id", ondelete="CASCADE"),
        nullable=False
    )
    current_balance: Mapped[int] = mapped_column(
        BIGINT,
        nullable=False,
    )
    goal_balance: Mapped[int] = mapped_column(
        BIGINT,
        nullable=False,
    )
    goal_date: Mapped[datetime] = mapped_column(
        postgresql.DATE, nullable=True
    )
    is_finished: Mapped[bool] = mapped_column(Boolean, default=False)
    created: Mapped[datetime] = mapped_column(
        postgresql.TIMESTAMP(timezone=True), nullable=True, default=datetime.datetime.now()
    )

    @staticmethod
    async def get_moneybox(moneybox_id: int) -> Union["MoneyBox", None]:
        async with async_session() as session:
            query = await session.execute(
                select(MoneyBox, Currency)
                .join(Currency, Currency.id == MoneyBox.currency_id)
                .where(MoneyBox.id == moneybox_id)
            )
            result = query.first()
            if result:
                moneybox, currency = result
                moneybox = moneybox.to_dict()
                moneybox["currency"] = currency
                return moneybox
