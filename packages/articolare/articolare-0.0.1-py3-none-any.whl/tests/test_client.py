import pytest
from unittest.mock import patch
from articolare import ArticolareClient

@patch('articolare.ArticolareClient._request')
def test_create(mock_request):
    mock_request.return_value = {"success": True}

    client = ArticolareClient(api_key="testkey")
    response = client.create(model="testmodel", prompt="testprompt", max_tokens=10)

    assert response == {"success": True}
    mock_request.assert_called_once_with("POST", "create", json={
        "model": "testmodel",
        "prompt": "testprompt",
        "max_tokens": 10
    })
