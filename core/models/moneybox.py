import datetime

from sqlalchemy.dialects import postgresql

from core.base import BaseModel

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, BIGINT, ForeignKey, Boolean


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
        postgresql.TIMESTAMP(timezone=True), nullable=True
    )
    is_finished: Mapped[bool] = mapped_column(Boolean, default=False)
    created: Mapped[datetime] = mapped_column(
        postgresql.TIMESTAMP(timezone=True), nullable=True
    )