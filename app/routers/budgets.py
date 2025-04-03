from types import NoneType

from fastapi import APIRouter, HTTPException
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



@router.get("/list/{user_id}", response_model=list[BudgetResponseSchema])
async def get_list(user_id: int):
    return await Budget.get_list(user_id=user_id)


@router.delete("/{budget_id}", response_model=NoneType)
async def delete_budget(budget_id: int):
    budget = await Budget.get_by_id(budget_id=budget_id)
    if budget:
        await budget.delete()
    else:
        raise HTTPException(status_code=404, detail="Budget not found")
