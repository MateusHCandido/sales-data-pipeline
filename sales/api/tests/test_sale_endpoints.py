import pytest
from httpx import AsyncClient
import sys
import os

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from main import app
from persistence.sale_repository import SaleRepository


@pytest.mark.asyncio
async def test_create_sale_order():
    sale_data = {
        'product_id': 1,
        'quantity': 5,
        'price_per_unit': 10.0
    }

    async with AsyncClient(app=app, base_url='http://localhost:8000') as ac:
        response = await ac.post('/sale', json=sale_data)

    assert response.status_code == 201
    assert response.json()['success'] is True

@pytest.mark.asyncio
async def test_cancel_sale_order():
    sale_id = 2

    async with AsyncClient(app=app, base_url='http://localhost:8000') as ac:
        response = await ac.put(f'/sale/{sale_id}')

    assert response.status_code == 200
    assert response.json()['success'] is True