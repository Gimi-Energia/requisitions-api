from unittest.mock import patch

import pytest

from apps.products.models import Product
from apps.products.service import ProductService


@pytest.fixture
def service():
    return ProductService()


@patch("apps.products.service.ProductService.list")
def test_list_products_with_mock(mock_list, service):
    params = {"offset_max": 10, "offset_min": 0}
    mock_list.return_value = {"total": 0, "products": []}
    data = service.list(**params)
    assert data["total"] == 0
    assert len(data["products"]) == 0
