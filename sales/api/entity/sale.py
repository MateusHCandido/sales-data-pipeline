from dataclasses import dataclass
from datetime import datetime
from sales.api.entity.sales_status import SaleStatus
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
    def to_dict(self):
        return {
            "product_id": self.product_id, 
            "quantity": self.quantity,
            "price_per_unit": self.price_per_unit,
            "sales_date": self.sales_date.isoformat() if isinstance(self.sales_date, datetime) else self.sales_date,
            "status": self.status.value
        }
    
    
class SaleOrderCreate(BaseModel):
    product_id: int
    quantity: int
    price_per_unit: float

    
        