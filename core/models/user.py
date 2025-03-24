import datetime

from sqlalchemy import BIGINT, String, Boolean, Integer
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import Mapped, mapped_column

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

