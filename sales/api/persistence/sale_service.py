from fastapi import HTTPException
from persistence.sale_repository import SaleRepository


class SaleService:

    def __init__(self, repository: SaleRepository):
        self.repository = repository

    
    def generate_sale_order(self, sale):
        sale.make_sale()    
        self.repository._save_sale(sale)
        #verify if having stock of product for quantity
        #producer message to stock service
        return "Sale order successfully created"


    def cancel_sale(self, sale_id: int):
        try:
            self.repository._update_sale(sale_id)
            return "Sale order successfully canceled"
        except:
            raise HTTPException(status_code=404, detail="Sale not found")
        #save the log of transaction on json
        #producer message to stock service
        #receive message from stock service informating canceling of product


       
