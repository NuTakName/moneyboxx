from enum import auto, StrEnum
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Enum, BIGINT, ForeignKey, select, and_

from core.base import BaseModel
from core.async_session import async_session


class CategoryTypeEnum(StrEnum):
    income = auto()
    expense = auto()


class Category(BaseModel):

    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    photo_path: Mapped[int] = mapped_column(String, nullable=True)
    type_ : Mapped[CategoryTypeEnum] = mapped_column(
        Enum(CategoryTypeEnum, name="category_type_enum"),
        nullable=False,
        index=True
    )
    name: Mapped[str] = mapped_column(String(180), nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=True)
    user_id: Mapped[int] = mapped_column(
        BIGINT, ForeignKey("users.id", ondelete="CASCADE"), nullable=True
    )


    @staticmethod
    async def get_category(user_id: int, type_: CategoryTypeEnum, name: str) -> "Category":
        async with async_session() as session:
            result = await session.execute(
                select(Category).where(
                    and_(
                        Category.user_id == user_id,
                        Category.type_ == type_,
                        Category.name == name
                    )
                )
            )
            return result.scalars().first()