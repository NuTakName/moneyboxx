import datetime
from sqlalchemy.dialects import postgresql

from core.base import BaseModel
from core.async_session import async_session

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, BIGINT, String, ForeignKey, select, desc


class Budget(BaseModel):

    __tablename__ = "budgets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(180), nullable=False)
    user_id: Mapped[int] = mapped_column(
        BIGINT,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=True
    )
    currency_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("currencies.id", ondelete="CASCADE"), nullable=False
    )
    created: Mapped[datetime] = mapped_column(
        postgresql.TIMESTAMP(timezone=True), nullable=False, default=datetime.datetime.now()
    )


    @staticmethod
    async def get_list(user_id: int) -> list["Budget"]:
        async with async_session() as session:
            result = await session.execute(
                select(Budget).where(Budget.user_id == user_id).order_by(desc(Budget.created))
            )
            return result.scalars().all()


    @staticmethod
    async def get_by_id(budget_id: int) -> "Budget":
        async with async_session() as session:
            result = await session.execute(
                select(Budget).where(Budget.id == budget_id)
            )
            return result.scalars().first()