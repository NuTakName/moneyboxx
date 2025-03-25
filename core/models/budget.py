import datetime
from sqlalchemy.dialects import postgresql

from core.base import BaseModel

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, BIGINT, String, ForeignKey


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