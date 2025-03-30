from fastapi import APIRouter, HTTPException

from app.schemas.operations import (
    OperationSchema,
    OperationResponseSchema,
    OperationAndCategoryResponseSchema
)
from core.models.operation import Operation

router = APIRouter(
    prefix="/operations",
    tags=["operations"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=OperationResponseSchema)
async def add_or_update_operation(data: OperationSchema):
    operation = await Operation.update_operation(
        budget_id=data.budget_id,
        value=data.value,
        category_id=data.category_id,
        description=data.description
    )
    if not operation:
        operation = Operation(
            budget_id=data.budget_id,
            type_=data.type_,
            value=data.value,
            description=data.description,
            category_id=data.category_id,
            sub_category_id=data.sub_category_id
        )
        operation = await operation.add()
    return operation


@router.get("/list/{current_budget_id}", response_model=list[OperationAndCategoryResponseSchema])
async def get_operations(current_budget_id: int):
    return await Operation.get_operations(current_budget_id=current_budget_id)
