import pytest

from product_db import ProductDB


@pytest.fixture
def product_db(scope='session'):
    db_path = 'tests/db/full_product_db.yaml'
    return ProductDB.from_yaml(db_path)