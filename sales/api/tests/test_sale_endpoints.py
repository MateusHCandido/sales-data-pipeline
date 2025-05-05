import pytest
from httpx import AsyncClient
from fastapi import status

from sales.api.routes.routes import router as sale_router



@pytest.mark.asyncio
async def test_create_sale_order():
    sale_data = {
        'product_id': 10,
        'quantity': 10,
        'price_per_unit': 10.0
    }

    async with AsyncClient(app=sale_router, base_url='http://localhost:8000') as ac:
        response = await ac.post('sale', json=sale_data)

    assert response.status_code == status.HTTP_201_CREATED

    json_response = response.json()
    
    assert json_response['success'] is True  
    assert json_response['message'] == "Sale order successfully created"
    
    data = json_response['data']
    assert data['product_id'] == sale_data['product_id']
    assert data['quantity'] == sale_data['quantity']
    assert data['price_per_unit'] == sale_data['price_per_unit']
    assert 'sales_date' in data
    assert data['status'] == ['SOLD']


@pytest.mark.asyncio
async def test_cancel_sale_order():
    sale_id = 1  # ID de venda existente para o teste

    async with AsyncClient(app=sale_router, base_url='http://localhost:8000') as ac:
        response = await ac.put(f'sale/{sale_id}')

    assert response.status_code == status.HTTP_200_OK

    json_response = response.json()
    assert json_response['success'] is True
    assert json_response['message'] == "Sale order successfully canceled"

    data = json_response['data']
    assert data['sale_id'] == str(sale_id)
    assert data['status'] == "CANCELED"
    assert 'timestamp' in data


@pytest.mark.asyncio
async def test_cancel_sale_order_not_found():
    sale_id = 99999999999

    async with AsyncClient(app=sale_router, base_url='http://localhost:8000') as ac:
        response = await ac.put(f'/sale/{sale_id}')

    assert response.status_code == status.HTTP_404_NOT_FOUND

    json_response = response.json()
    assert json_response['success'] is False
    assert json_response['message'] == "Sale not found"
    assert json_response['data']['sale_id'] == str(sale_id)
    assert json_response['data']['status'] == "CANCELED"
    assert 'timestamp' in json_response['data']