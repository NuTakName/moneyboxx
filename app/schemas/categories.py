from pydantic import BaseModel, Field

from core.models.category import CategoryTypeEnum


class CategorySchema(BaseModel):
    photo_path: str | None = None
    type_: CategoryTypeEnum
    name: str
    description: str | None = None
    user_id: int = Field(ge=0)


class CategoryResponseSchema(CategorySchema):
    id: int = Field(ge=0)