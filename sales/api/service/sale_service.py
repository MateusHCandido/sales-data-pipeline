from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from sales.api.persistence.sale_repository import sales_repository
from sales.api.entity.sale import Sale

from datetime import datetime

from sales.api.service.logger_service import generate_result_log


class SaleService:

    def __init__(self, repository):
        self.repository = repository

    
    def generate_sale_order(self, sale: Sale):
        try:
            sale.make_sale()    
            self.repository._save_sale(sale)
            success_message = "Sale order successfully created"
            status_code = status.HTTP_201_CREATED

            response = self.generate_response(status_code, sale.to_dict(), success_message, success=True)
            generate_result_log(response, type_log='info')

            return response
        
        except HTTPException as http_exc:
            raise http_exc
        
        except Exception as exc:
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR

            response = self.generate_response(status_code, sale.to_dict(), str(exc))
            generate_result_log(response, type_log='error')
            
            return response

    def cancel_sale(self, sale_id: int):
        data = {'sale_id': sale_id, 'status': 'CANCELED', 'timestamp': datetime.utcnow().isoformat()}
        try:
            self.repository._cancel_sale(sale_id)
            status_code = status.HTTP_200_OK
            success_message = "Sale order successfully canceled"
            response = self.generate_response(status_code, data, success_message, success=True)

            generate_result_log(response, 'info')
            return response
        except HTTPException as http_exc:
            raise http_exc
        except Exception as exc:
            status_code=status.HTTP_404_NOT_FOUND
            message = "Sale not found"
            response = self.generate_response(status_code, data, message)
            generate_result_log(response, type_log='error')
            
            return response


    def generate_response(self, status_code, data, message, success=False):
        if success is True:
            return JSONResponse(
                status_code= status_code,
                content={"success": True, 
                        "data": data,
                        "message": str(message)
                    }   
                )

        return JSONResponse(
                status_code= status_code,
                content={"success": False, 
                        "data": data,
                        "message": str(message)
                    }   
                )


sale_service = SaleService(sales_repository)

       
