from fastapi import APIRouter, HTTPException

from app.schemas.moneybox import MoneyboxResponseSchema, MoneyboxSchema, GetMoneyboxResponseSchema
from core.models.moneybox import MoneyBox


router = APIRouter(
    prefix="/moneybox",
    tags=["moneybox"],
    responses={404: {"description": "Not found"}},
)

@router.get("/{moneybox_id}", response_model=GetMoneyboxResponseSchema)
async def get_moneybox(moneybox_id: int):
    moneybox = await MoneyBox.get_moneybox(moneybox_id=moneybox_id)
    if moneybox:
        return moneybox
    else:
        raise HTTPException(status_code=404, detail="Moneybox not found")



@router.post("/", response_model=MoneyboxResponseSchema)
async def add_moneybox(data: MoneyboxSchema):
    moneybox = MoneyBox(
        user_id=data.user_id,
        name=data.name,
        currency_id=data.currency_id,
        current_balance=data.current_balance,
        goal_balance=data.goal_balance,
        goal_date=data.goal_date
    )
    return await moneybox.add()