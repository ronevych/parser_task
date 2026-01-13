import pytest
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    """
    fixture gives us ready client. We will be able to
    test something(api client).
    """
    return APIClient()
