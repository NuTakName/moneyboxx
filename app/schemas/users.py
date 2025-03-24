from pydantic import BaseModel, Field
from datetime import datetime


class UserSchema(BaseModel):
    id: int = Field(ge=0)
    name: str


class UserResponseSchema(UserSchema):
    registration_date: datetime
    is_premium: bool
    is_pro: bool
    is_admin: bool
    money: int = Field(ge=0)
    get_bonus: bool
