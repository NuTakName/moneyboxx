import datetime
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Enum, ForeignKey, BIGINT, select, update, and_

from app.schemas.operations import UpdateOperationSchema
from core.base import BaseModel
from core.async_session import async_session
from core.models.category import CategoryTypeEnum, Category
from core.models.currency import Currency
from core.models.budget import Budget


class Operation(BaseModel):

    __tablename__ = "operations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    budget_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("budgets.id", ondelete="CASCADE"),
        nullable=False
    )
    type_: Mapped[CategoryTypeEnum] = mapped_column(
        Enum(CategoryTypeEnum, name="category_type_enum"),
        nullable=False,
        index=True
    )
    date: Mapped[datetime] = mapped_column(
        postgresql.TIMESTAMP(timezone=True),
        default=datetime.datetime.now()
    )
    value: Mapped[int] = mapped_column(
        BIGINT,
        nullable=False,
    )
    description: Mapped[str] = mapped_column(String, nullable=True)
    category_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("categories.id", ondelete="CASCADE"),
        nullable=False
    )
    sub_category_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("categories.id", ondelete="CASCADE"),
        nullable=True
    )


    @staticmethod
    async def get_operations(current_budget_id: int) -> list[dict]:
        async with async_session() as session:
            result = await session.execute(
                select(Operation, Category, Currency)
                .join(Category, Category.id == Operation.category_id)
                .join(Budget, Budget.id == Operation.budget_id)
                .join(Currency, Currency.id == Budget.currency_id)
                .where(Operation.budget_id == current_budget_id)
            )
            data = {}
            for operation, category, currency in result.all():
                if category.id not in data:
                    operation = operation.to_dict()
                    operation["category_name"] = category.name
                    operation["currency_code"] = currency.code
                    operation["currency_symbol"] = currency.symbol
                    data[category.id] = operation
                else:
                    data[category.id]["value"] += operation.value
            return list(data.values())


    @staticmethod
    async def get_operation_by_category_id(category_id: int) -> list[dict]:
        async with async_session() as session:
            result = await session.execute(
                select(Operation, Category.name, Currency)
                .join(Category, Category.id == Operation.category_id)
                .join(Budget, Budget.id == Operation.budget_id)
                .join(Currency, Currency.id == Budget.currency_id)
                .where(Operation.category_id == category_id)
            )
            results = []
            for operation, category_name, currency in result.all():
                operation = operation.to_dict()
                operation["category_name"] = category_name
                operation["currency_code"] = currency.code
                operation["currency_symbol"] = currency.symbol
                results.append(operation)
            return results



    @staticmethod
    async def get_operation_by_id(operation_id: int) -> "Operation":
        async with async_session() as session:
            result = await session.execute(
                select(Operation).where(Operation.id == operation_id)
            )
            return result.scalars().first()


    @staticmethod
    async def update_operation(operation: UpdateOperationSchema) -> "Operation":
        async with async_session() as session:
            result = await session.execute(
                update(Operation).where(Operation.id == operation.id)
                .values(**operation.model_dump())
                .returning(Operation)
            )
            await session.commit()
            operation = result.scalars().first()
            if operation:
                await session.refresh(operation)
                return operation
