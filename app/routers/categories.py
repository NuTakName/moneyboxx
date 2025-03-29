from fastapi import APIRouter, HTTPException

from app.schemas.categories import CategorySchema, CategoryResponseSchema
from core.models.category import Category, CategoryTypeEnum

router = APIRouter(
    prefix="/categories",
    tags=["categories"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=CategoryResponseSchema)
async def add_category(data: CategorySchema):
    category = Category(
        photo_path=data.photo_path,
        type_=data.type_,
        name=data.name,
        description=data.description,
        user_id=data.user_id
    )
    return await category.add()


@router.get("/{user_id}/{type_}/{name}", response_model=CategoryResponseSchema)
async def get_category(user_id: int, type_: CategoryTypeEnum, name: str):
    category = await Category.get_category(
        user_id=user_id, type_=type_, name=name
    )
    if category:
        return category
    else:
        raise HTTPException(status_code=404, detail="Category not found")