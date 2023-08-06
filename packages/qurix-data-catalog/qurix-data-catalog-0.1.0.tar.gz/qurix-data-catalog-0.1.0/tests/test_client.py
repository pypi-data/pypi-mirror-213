from qurix.data.catalog.client import DataCatalogClient
import pytest


@pytest.fixture
def client() -> DataCatalogClient:
    return DataCatalogClient(name="sample")


def test_client_name(client: DataCatalogClient):
    result = client.name
    assert result == "sample"
