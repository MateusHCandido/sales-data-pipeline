from fastapi import FastAPI
from sales.api.routes.routes import router as sale_router


app = FastAPI()


app.include_router(sale_router, prefix="/api", tags=["sales"])



    








