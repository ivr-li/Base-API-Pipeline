from datetime import datetime, timezone

import requests
from requests.exceptions import ConnectionError, Timeout

from src.config import config
from src.database import DB
from src.logger import logger_errors

URL = f"https://v6.exchangerate-api.com/v6/{config.API_KEY}/latest/USD"


def baseline(db: DB):
    """Initialize the data baseline"""
    try:
        response = requests.get(URL, timeout=10)
    except ConnectionError as ex:
        logger_errors.error(f"Exchangerate-api.com - connection error: {ex}")
        return
    except Timeout as ex:
        logger_errors.error(f"Exchangerate-api.com - timeout: {ex}")
        return

    requests_data = response.json()
    request_status = requests_data.get("result")

    if request_status == "success":
        request_id = db._insert_request(
            base_code=requests_data.get("base_code", ""), request_status=request_status
        )
        date = requests_data.get("time_last_update_unix")
        db._insert_rates(
            request_id=request_id,
            date=datetime.fromtimestamp(date, tz=timezone.utc).date(),
            rates=requests_data.get("conversion_rates"),
        )

    else:
        db._insert_request(
            base_code=requests_data.get("base_code", "error"),
            request_status=request_status,
        )
