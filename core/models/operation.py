import datetime
from typing import Union

from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import (
    Integer,
    String,
    Enum,
    ForeignKey,
    BIGINT,
    select,
    update,
    and_,
    extract,
    func,
    case,
    desc
)

from app.schemas.operations import UpdateOperationSchema
from core.base import BaseModel
from core.async_session import async_session
from core.models.category import CategoryTypeEnum, Category
from core.models.currency import Currency
from core.models.budget import Budget
from core.models.user import User
from core.models.moneybox import MoneyBox


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
    async def get_operations(current_budget_id: int, month: int) -> list[dict]:
        async with async_session() as session:
            result = await session.execute(
                select(Operation, Category, Currency)
                .join(Category, Category.id == Operation.category_id)
                .join(Budget, Budget.id == Operation.budget_id)
                .join(Currency, Currency.id == Budget.currency_id)
                .where(
                    and_(
                        Operation.budget_id == current_budget_id,
                        extract("month", Operation.date) == month,
                    ))
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
    async def get_operation_by_category_id_or_type(
        month: int, type_: CategoryTypeEnum | None = None, category_id: int | None = None
    ) -> list[dict]:
        conditions = [extract("month", Operation.date) == month]
        if category_id:
            conditions.append(Operation.category_id == category_id)
        if type_:
            conditions.append(Operation.type_ == type_)
        async with async_session() as session:
            result = await session.execute(
                select(Operation, Category.name, Currency)
                .join(Category, Category.id == Operation.category_id)
                .join(Budget, Budget.id == Operation.budget_id)
                .join(Currency, Currency.id == Budget.currency_id)
                .where(and_(*conditions))
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
    async def update_operation(operation: UpdateOperationSchema) -> Union["Operation", None]:
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


    @staticmethod
    async def get_total_amount(month: int, current_budget_id: int) -> dict:
        async with async_session() as session:
            query = await session.execute(
                select(
                    func.sum(case((and_(
                        Operation.type_ == CategoryTypeEnum.income,
                        extract("month", Operation.date) == month,
                        Operation.budget_id == current_budget_id), Operation.value),
                        else_=0)),
                    func.sum(case((and_(
                        Operation.type_ == CategoryTypeEnum.expense,
                        extract("month", Operation.date) == month,
                        Operation.budget_id == current_budget_id), Operation.value),
                        else_=0))
                )
            )
            result = query.first()
            data = {
                "total_amount_income": result[0],
                "total_amount_expense": result[1]
            }
            return data


    @staticmethod
    async def get_difference(current_budget_id: int) -> dict:
        async with async_session() as session:
            query = await session.execute(
                select(
                func.sum(case((and_(
                    Operation.type_ == CategoryTypeEnum.income,
                    Operation.budget_id == current_budget_id), Operation.value),
                    else_=0)),
                func.sum(case((and_(
                    Operation.type_ == CategoryTypeEnum.expense,
                    Operation.budget_id == current_budget_id), Operation.value),
                    else_=0))
            ))
            result = query.first()
            data = {"difference": result[0] - result[1]}
            return data


    @staticmethod
    async def get_statistic(user_id: int) -> Union[dict, None]:
        async with async_session() as session:
            query = await session.execute(
                select(
                    func.sum(case((and_(
                        Operation.type_ == CategoryTypeEnum.income,
                        Operation.budget_id == User.current_budget), Operation.value),
                        else_=0)),
                    func.sum(case((and_(
                        Operation.type_ == CategoryTypeEnum.expense,
                        Operation.budget_id == User.current_budget), Operation.value),
                        else_=0)),
                    func.count(MoneyBox.id.distinct())
                    .filter(MoneyBox.user_id == user_id, MoneyBox.is_finished.is_(True)),
                    Currency
                )
                .join(User, User.current_budget == Operation.budget_id)
                .outerjoin(MoneyBox, MoneyBox.user_id == User.id)
                .join(Budget, Budget.id == Operation.budget_id)
                .join(Currency, Currency.id == Budget.currency_id)
                .where(User.id == user_id)
                .group_by(Currency)
            )
            result = query.first()
            data = {}
            if result:
                total_amount_income, total_amount_expense, count_moneybox, currency = result
                data["total_amount_income"] = total_amount_income
                data["total_amount_expense"] = total_amount_expense
                data["count_moneybox"] = count_moneybox
                data["currency"] = currency
                return data



    @staticmethod
    async def get_statistic_for_period(user_id: int, month: int, year: int) -> list[dict]:
        conditions = [User.id == user_id]
        if month:
            conditions.append(extract("month", Operation.date) == month)
        if year:
            conditions.append(extract("year", Operation.date) == year)
        async with async_session() as session:
            query = await session.execute(
                select(Operation, Category.name, Currency)
                .join(User, User.current_budget == Operation.budget_id)
                .join(Category, Category.id == Operation.category_id)
                .join(Budget, Budget.id == Operation.budget_id)
                .join(Currency, Currency.id == Budget.currency_id)
                .where(and_(*conditions))
                .order_by(desc(Operation.value))
            )
            result = []
            for operation, category_name, currency in query.all():
                operation = operation.to_dict()
                operation["category_name"] = category_name
                operation["currency"] = currency
                result.append(operation)
            return result


    @staticmethod
    async def get_list_operations(user_id: int) -> list["Operation"]:
        async with async_session() as session:
            result = await session.execute(
                select(Operation)
                .join(User, User.current_budget == Operation.budget_id)
                .where(User.id == user_id)
            )
            return result.scalars().all()