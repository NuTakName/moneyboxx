from fastapi import APIRouter, HTTPException

from app.schemas.operations import OperationSchema, OperationResponseSchema
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
