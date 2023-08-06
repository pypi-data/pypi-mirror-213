import asyncio
import logging

import httpx

from contact_magic.utils import find_item
from settings import SETTINGS

logging.getLogger("httpx").setLevel(logging.WARNING)


endpoint = "https://app.copyfactory.io/api/v2/generate/"

headers = {"Accept": "application/json", "Authorization": SETTINGS.COPYFACTORY_API_KEY}


def _get_rate_limit_sleep_time(response):
    """Get rate limit window expiration time from response if the response
    status code is 429.
    """
    try:
        data = response.headers
        if "Retry-After" in data.keys():
            return int(data["Retry-After"])
    except (AttributeError, KeyError, ValueError):
        return 60


async def make_copyfactory_request(premise_id: int, variables: dict, max_retries=3):
    if not SETTINGS.COPYFACTORY_API_KEY:
        return None
    data = {
        "premise_id": premise_id,
        "variables": variables,
    }
    try:
        session = httpx.AsyncClient(timeout=90)
        retries = 0
        while retries < max_retries:
            res = await session.request(
                method="POST", url=endpoint, headers=headers, json=data
            )
            if res.status_code == 429:
                await asyncio.sleep(_get_rate_limit_sleep_time(res))
                retries += 1
                continue

            if res.status_code == 200:
                response_data = res.json()["data"]
                if response_data["status"] == "success":
                    return response_data
                if response_data["status"] == "error":
                    required_variables = response_data["meta_data"]["sentence_premise"][
                        "required_variables"
                    ]
                    for req_var in required_variables:
                        if item := find_item(variables, req_var):
                            data["variables"][req_var] = str(item)
                    if not data["variables"].get("company_organization_name"):
                        data["variables"]["company_organization_name"] = ""

            retries += 1
        return None
    except Exception:
        return None
