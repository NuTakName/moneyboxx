from fastapi import APIRouter, HTTPException

from app.schemas.currency import CurrencySchema, CurrencyResponseSchema
from core.models.currency import Currency


router = APIRouter(
    prefix="/currency",
    tags=["currency"],
    responses={404: {"description": "Not found"}},
)


@router.post('/', response_model=CurrencyResponseSchema)
async def add_currency(data: CurrencySchema):
    currency = Currency(
        name=data.name,
        code=data.code,
        type_=data.type_,
        symbol=data.symbol
    )
    return await currency.add()


@router.get('/by_name/{name}')
async def get_by_name(name: str):
    currency = await Currency.get_by_name(name=name)
    if currency:
        return currency
    else:
        raise HTTPException(status_code=404, detail="Currency not found")