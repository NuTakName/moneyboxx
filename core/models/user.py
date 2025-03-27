import datetime

from sqlalchemy import BIGINT, String, Boolean, Integer, select, ForeignKey, update
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import Mapped, mapped_column

from core.async_session import async_session
from core.base import BaseModel


class User(BaseModel):

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    registration_date: Mapped[datetime] = mapped_column(
        postgresql.TIMESTAMP(timezone=True),
        default=datetime.datetime.now()
    )
    is_premium: Mapped[bool] = mapped_column(Boolean, default=False)
    is_pro: Mapped[bool] = mapped_column(Boolean, default=False)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    money: Mapped[int] = mapped_column(Integer, default=100, server_default='100', nullable=False)
    get_bonus: Mapped[bool] = mapped_column(Boolean, default=False, server_default='false', nullable=False)
    current_budget: Mapped[int] = mapped_column(Integer, ForeignKey("budgets.id"), nullable=True)
    current_moneybox: Mapped[int] = mapped_column(Integer, ForeignKey("moneybox.id"), nullable=True)



    @staticmethod
    async def get_user(user_id: int) -> "User":
        async with async_session() as session:
            result = await session.execute(
                select(User).where(User.id == user_id)
            )
            return result.scalars().first()


    @staticmethod
    async def set_current_budget(user_id: int, current_budget: int) -> "User":
        async with async_session() as session:
            result = await session.execute(
                update(User).where(User.id == user_id)
                .values(current_budget=current_budget)
                .returning(User)
            )
            return result.scalars().first()
