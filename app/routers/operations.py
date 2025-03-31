from types import NoneType

from fastapi import APIRouter, HTTPException

from app.schemas.operations import (
    OperationSchema,
    OperationResponseSchema,
    OperationAndCategoryResponseSchema,
    UpdateOperationSchema,
    OperationTotalAmount
)
from core.models.operation import Operation

router = APIRouter(
    prefix="/operations",
    tags=["operations"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=OperationResponseSchema)
async def add_operation(data: OperationSchema):
    operation = Operation(
        budget_id=data.budget_id,
        type_=data.type_,
        value=data.value,
        description=data.description,
        category_id=data.category_id,
        sub_category_id=data.sub_category_id
    )
    return await operation.add()


@router.put("/", response_model=OperationResponseSchema)
async def update_operation(data: UpdateOperationSchema):
    operation = await Operation.update_operation(operation=data)
    if operation:
        return operation
    else:
        raise HTTPException(status_code=404, detail="Operation not found")


@router.get("/list/{current_budget_id}/{month}", response_model=list[OperationAndCategoryResponseSchema])
async def get_operations(current_budget_id: int, month: int):
    return await Operation.get_operations(current_budget_id=current_budget_id, month=month)

#todo добавить поиск по месяцу
@router.get('/list_by_category_id/{category_id}', response_model=list[OperationAndCategoryResponseSchema])
async def get_operations_by_category_id(category_id: int):
    return await Operation.get_operation_by_category_id(category_id=category_id)


@router.delete("/{operation_id}", response_model=NoneType)
async def delete_operation(operation_id: int):
    operation = await Operation.get_operation_by_id(operation_id=operation_id)
    if operation:
        await operation.delete()
    else:
        raise HTTPException(status_code=404, detail="Operation not found")


@router.get("/total_amount/{month}/{current_budget_id}", response_model=OperationTotalAmount)
async def get_total_amount(month: int, current_budget_id: int):
    total_amount = await Operation.get_total_amount(
        month=month, current_budget_id=current_budget_id
    )
    return total_amount