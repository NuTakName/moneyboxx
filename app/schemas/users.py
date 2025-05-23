from pydantic import BaseModel, Field
from datetime import datetime


class UserSchema(BaseModel):
    id: int = Field(ge=0)
    name: str
    current_budget: int | None = None
    current_moneybox: int | None = None



class UserResponseSchema(UserSchema):
    registration_date: datetime
    is_premium: bool
    is_pro: bool
    is_admin: bool
    money: int = Field(ge=0)
    get_bonus: bool
    current_budget: int | None = None
    current_moneybox: int | None = None


class UserCurrentBudget(BaseModel):
    user_id: int = Field(ge=0)
    current_budget: int = Field(ge=0)


class UserMoneyboxSchema(BaseModel):
    user_id: int = Field(ge=0)
    current_moneybox: int = Field(ge=0)

class BonusSchema(BaseModel):
    user_id: int = Field(ge=0)
    money: int = Field(ge=0)