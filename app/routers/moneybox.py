from types import NoneType

from fastapi import APIRouter, HTTPException

from app.schemas.moneybox import (
    MoneyboxResponseSchema,
    MoneyboxSchema,
    GetMoneyboxResponseSchema,
    UpdateCurrentBalanceSchema
)
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


@router.patch("/update_current_balance", response_model=MoneyboxResponseSchema)
async def update_current_balance(data: UpdateCurrentBalanceSchema):
    moneybox = await MoneyBox.update_current_balance(
        moneybox_id=data.id, amount=data.amount, is_finished=data.is_finished
    )
    if moneybox:
        return moneybox
    else:
        raise HTTPException(status_code=404, detail="Moneybox not found")



@router.get("/list/{user_id}", response_model=list[MoneyboxResponseSchema])
async def get_list_moneybox(user_id: int):
    return await MoneyBox.get_list(user_id=user_id)


@router.delete('/{moneybox_id}', response_model=NoneType)
async def delete_moneybox(moneybox_id: int):
    moneybox = await MoneyBox.get(moneybox_id=moneybox_id)
    if moneybox:
        await moneybox.delete()
    else:
        raise HTTPException(status_code=404, detail="Moneybox not found")