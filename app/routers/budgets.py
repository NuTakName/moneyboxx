from fastapi import APIRouter
from core.models.budget import Budget

from app.schemas.budgets import BudgetSchema, BudgetResponseSchema

router = APIRouter(
    prefix="/budgets",
    tags=["budgets"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=BudgetResponseSchema)
async def add_budget(data: BudgetSchema):
    budget = Budget(
        name=data.name,
        user_id=data.user_id,
        currency_id=data.currency_id
    )
    return await budget.add()
