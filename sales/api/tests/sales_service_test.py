import pytest
from unittest.mock import MagicMock, patch
from fastapi import status
from sales.api.entity.sale import Sale
from sales.api.service.sale_service import SaleService
from datetime import datetime
import json


@pytest.fixture
def mock_repository():
    return MagicMock()


@pytest.fixture
def sale_service(mock_repository):
    return SaleService(mock_repository)


@pytest.fixture
def sample_sale():
    return Sale(
        sale_id=1,
        product_id=1,
        quantity=2,
        price_per_unit=10.0,
        sales_date=datetime.utcnow(),
        status="SOLD"
    )


@patch("sales.api.service.sale_service.generate_result_log")
def test_generate_sale_order_success(mock_log, sale_service, sample_sale):
    response = sale_service.generate_sale_order(sample_sale)

    body = json.loads(response.body.decode())

    assert response.status_code == status.HTTP_201_CREATED
    assert body["success"] is True
    assert body["message"] == "Sale order successfully created"
    assert body["data"]["product_id"] == 1


@patch("sales.api.service.sale_service.generate_result_log")
def test_generate_sale_order_exception(mock_log, sale_service, sample_sale):
    sale_service.repository._save_sale.side_effect = Exception("DB error")

    response = sale_service.generate_sale_order(sample_sale)

    body = json.loads(response.body.decode())

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert body["success"] is False
    assert "DB error" in body["message"]


@patch("sales.api.service.sale_service.generate_result_log")
def test_cancel_sale_success(mock_log, sale_service):
    sale_id = 1
    response = sale_service.cancel_sale(sale_id)

    body = json.loads(response.body.decode())

    assert response.status_code == status.HTTP_200_OK
    assert body["success"] is True
    assert body["data"]["status"] == "CANCELED"


@patch("sales.api.service.sale_service.generate_result_log")
def test_cancel_sale_not_found(mock_log, sale_service):
    sale_id = 9999
    sale_service.repository._cancel_sale.side_effect = Exception("Sale not found")

    response = sale_service.cancel_sale(sale_id)

    body = json.loads(response.body.decode())

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert body["success"] is False
    assert body["message"] == "Sale not found"
