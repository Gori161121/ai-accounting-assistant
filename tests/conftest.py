import pytest

from backend.data_loader import load_data


@pytest.fixture(scope="session")
def data():
    return load_data()
