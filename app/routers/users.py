from fastapi import APIRouter, HTTPException
from core.models.user import User
from app.schemas.users import UserSchema, UserResponseSchema, UserCurrentBudget, BonusSchema, UserMoneyboxSchema

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=UserResponseSchema)
async def add_user(data: UserSchema):
    user = User(
        id=data.id,
        name=data.name,
        current_moneybox=data.current_moneybox,
        current_budget=data.current_budget
    )
    return await user.add()


@router.get("/{user_id}", response_model=UserResponseSchema)
async def get_user(user_id: int):
    user = await User.get_user(user_id=user_id)
    if user:
        return user
    else:
        raise HTTPException(status_code=404, detail="User not found")


@router.patch("/set_current_budget", response_model=UserResponseSchema)
async def set_current_budget(data: UserCurrentBudget):
    user = await User.set_current_budget(user_id=data.user_id, current_budget=data.current_budget)
    if user:
        return user
    else:
        raise HTTPException(status_code=404, detail="User not found")



@router.patch("/collect_bonus", response_model=UserResponseSchema)
async def get_bonus(data: BonusSchema):
    user = await User.collect_bonus(user_id=data.user_id, money=data.money)
    if user:
        return user
    else:
        raise HTTPException(status_code=404, detail="User not found")


@router.patch("/set_current_moneybox", response_model=UserResponseSchema)
async def set_current_moneybox(data: UserMoneyboxSchema):
    user = await User.set_current_moneybox(user_id=data.user_id, current_moneybox=data.current_moneybox)
    if user:
        return user
    else:
        raise HTTPException(status_code=404, detail="User not found")