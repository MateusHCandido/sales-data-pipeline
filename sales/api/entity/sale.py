from dataclasses import dataclass
from datetime import datetime
from entity.sales_status import SaleStatus
from pydantic import BaseModel
import uuid


@dataclass
class Sale:
    sale_id: int
    product_id: int
    quantity: int
    price_per_unit: float
    sales_date: datetime
    status: SaleStatus

    # def __init__(self, sale):
    #     self.sale_id = sale['sale_id']
    #     self.product_id = sale['product_id']
    #     self.quantity = sale['quantity']
    #     self.price_per_unit = sale['price_per_unit']
    #     self.sales_date = sale['sales_date']
    #     self.status = sale['status']

    def make_sale(self):
        self.status = SaleStatus.SOLD
        
    def cancel_sale(self):
        self.status = SaleStatus.CANCELED

    def generate_id() -> int:
        return uuid.uuid4().int >> 64

    @classmethod
    def convert_to_entity(cls, dto):
        return cls(
            sale_id=Sale.generate_id(),
            product_id=dto.product_id,
            quantity=dto.quantity,
            price_per_unit=dto.price_per_unit,
            sales_date=datetime.utcnow(),
            status=SaleStatus.PENDING   
        )
    
    
class SaleOrderCreate(BaseModel):
    product_id: int
    quantity: int
    price_per_unit: float

    
        