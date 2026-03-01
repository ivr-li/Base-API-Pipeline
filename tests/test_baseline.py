import json
from unittest.mock import MagicMock, patch

import pytest
from requests.exceptions import ConnectionError, Timeout

from src.baseline import baseline


@pytest.fixture
def api_response():
    with open("tests/data.json") as f:
        return json.load(f)


@pytest.fixture
def mock_db():
    return MagicMock()


# ====================================
# Positive
# ====================================


# Successful API response: request and rates are saved
@patch("src.baseline.requests.get")
def test_baseline_success(mock_get, mock_db, api_response):
    mock_get.return_value.json.return_value = api_response
    mock_db._insert_request.return_value = 1

    baseline(mock_db)

    mock_db._insert_request.assert_called_once_with(
        base_code="USD", request_status="success"
    )
    mock_db._insert_rates.assert_called_once()


# ====================================
# Negative
# ====================================


# API returned error status: only request is saved
@patch("src.baseline.requests.get")
def test_baseline_error_status(mock_get, mock_db):
    mock_get.return_value.json.return_value = {
        "result": "error",
        "base_code": "USD",
    }

    baseline(mock_db)

    mock_db._insert_request.assert_called_once_with(
        base_code="USD", request_status="error"
    )
    mock_db._insert_rates.assert_not_called()


# Connection error
@patch("src.baseline.requests.get")
def test_baseline_connection_error(mock_get, mock_db):
    mock_get.side_effect = ConnectionError("connection failed")

    baseline(mock_db)

    mock_db._insert_request.assert_not_called()


# Request timeout
@patch("src.baseline.requests.get")
def test_baseline_timeout(mock_get, mock_db):
    mock_get.side_effect = Timeout("request timed out")

    baseline(mock_db)

    mock_db._insert_request.assert_not_called()
