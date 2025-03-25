from fastapi import APIRouter, HTTPException
from core.models.user import User
from app.schemas.users import UserSchema, UserResponseSchema

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