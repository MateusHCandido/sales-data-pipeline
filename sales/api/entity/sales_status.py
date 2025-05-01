from enum import Enum

class SaleStatus(Enum):
    PENDING = 'PENDING',
    SOLD = 'SOLD',
    CANCELED = 'CANCELED'