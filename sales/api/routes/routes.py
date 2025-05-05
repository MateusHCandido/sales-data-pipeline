from fastapi import APIRouter

from sales.api.entity.sale import Sale, SaleOrderCreate
from sales.api.service.sale_service import sale_service


router = APIRouter()

@router.post('/sale')
async def generate_sale_order(sale_dto: SaleOrderCreate):
    sale = Sale.convert_to_entity(sale_dto)
    return sale_service.generate_sale_order(sale)
     

@router.put('/sale/{sale_id}')
async def cancel_sale_order(sale_id):
    return sale_service.cancel_sale(sale_id)