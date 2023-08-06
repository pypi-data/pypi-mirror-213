import asyncio
import logging

import httpx

from contact_magic.utils import fix_website
from settings import SETTINGS

logging.getLogger("httpx").setLevel(logging.WARNING)

base_url = "https://salesscrapers.dev/api/"

headers = {"Accept": "application/json", "X-API-Key": SETTINGS.SALES_SCRAPERS_API_KEY}


async def make_sales_scraper_request(endpoint, data: dict, max_retries=3):
    if not SETTINGS.SALES_SCRAPERS_API_KEY:
        return None
    url = f"{base_url}{endpoint}"
    try:
        session = httpx.AsyncClient(timeout=120)
        retries = 0
        while retries < max_retries:
            res = await session.request(
                method="get", url=url, headers=headers, params=data
            )
            if res.status_code == 200:
                return res.json()
            if res.status_code == 422:
                validation_errors = res.json().get("detail")
                for error in validation_errors:
                    if error.get("type") == "value_error.url.scheme":
                        error_key = error.get("loc")[1]
                        if error_key in data:
                            data[error_key] = fix_website(data[error_key])
            await asyncio.sleep(1)
            retries += 1
        return None
    except Exception:
        return None
