from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse

from persistence.sale_repository import SaleRepository
from persistence.sale_service import SaleService
from entity.sale import Sale, SaleOrderCreate



db_config = {
    "dbname": "sales_db",
    "user": "user",
    "password": "password",
    "host": "localhost",
    "port": 5432
}

app = FastAPI()
repository = SaleRepository(db_config)
sale_service = SaleService(repository)

@app.post('/sale')
async def generate_sale_order(sale_dto: SaleOrderCreate):
    try:
        sale = Sale.convert_to_entity(sale_dto)
        result = sale_service.generate_sale_order(sale)
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={"success": True, "data": result}
    )
    except HTTPException as http_exc:
        raise http_exc
    except Exception as exc:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"success": False, "message": str(exc)}
        )

@app.put('/sale/{sale_id}')
async def update_sale_order(sale_id: int):
    try:
        result = sale_service.cancel_sale(sale_id)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"success": True, "data": result}
        )
    except HTTPException as http_exc:
        raise http_exc
    except Exception as exc:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"success": False, "message": str(exc)}
        )


    








