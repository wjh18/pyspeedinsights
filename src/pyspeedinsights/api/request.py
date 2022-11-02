"""Async request preparation and processing for PSI API calls."""

import asyncio
from collections import Counter
from typing import Any, Coroutine, Union

import aiohttp

from ..utils.generic import remove_nonetype_dict_items
from ..utils.urls import validate_url
from .keys import get_api_key

next_delay = 1  # Global for applying a 1s delay between requests


async def get_response(
    url: str,
    category: str = None,
    locale: str = None,
    strategy: str = None,
    utm_campaign: str = None,
    utm_source: str = None,
    captcha_token: str = None,
) -> dict:
    """Makes async GET calls to the PSI API for the requested page's URL.

    Args of NoneType will not be added as query params. They'll use PSI API defaults.

    Returns:
        The awaited json response from the server as a str.
    Raises:
        aiohttp.ClientError: The retry limit was reached for failed requests.
    """
    base_url = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"
    url = validate_url(url)
    params = {
        "url": url,
        "category": category,
        "locale": locale,
        "strategy": strategy,
        "utm_campaign": utm_campaign,
        "utm_source": utm_source,
        "captcha_token": captcha_token,
    }
    # Use API defaults instead of passing None values as query params.
    params = remove_nonetype_dict_items(params)
    params["key"] = get_api_key()
    req_url = params["url"]

    # Add a 1s delay between calls to avoid 500 errors from server.
    global next_delay
    next_delay += 1
    await asyncio.sleep(next_delay)

    print(f"Sending request... ({req_url})")
    # Make async call with query params to PSI API and await response.
    async with aiohttp.ClientSession() as session:
        async with session.get(url=base_url, params=params) as resp:
            json_resp = None
            retry_attempts = 5
            while json_resp is None:
                try:
                    resp.raise_for_status()
                    json_resp = await resp.json()
                    print(f"Request successful! ({req_url})")
                except aiohttp.ClientError as err_c:
                    if retry_attempts < 1:
                        print(err_c)
                        print(f"Retry limit reached. Skipping ({req_url})")
                        raise aiohttp.ClientError(err_c)
                    else:
                        retry_attempts -= 1
                        print(
                            "Request failed. Retrying... ",
                            f"{retry_attempts} retries left ({req_url})",
                        )
                        await asyncio.sleep(1)
    return json_resp


def run_requests(
    request_urls: list[str], api_args_dict: dict[str, Union[str, None]]
) -> list[dict]:
    """Runs async requests to PSI API and gathers responses.

    Called within main() in pyspeedinsights.app.
    """
    tasks = get_tasks(request_urls, api_args_dict)
    return asyncio.run(gather_responses(tasks))


async def gather_responses(tasks: list[Coroutine]) -> list[dict]:
    """Gathers tasks and awaits the return of the responses for processing."""
    print(f"Preparing {len(tasks)} URL(s)...")
    responses = await asyncio.gather(*tasks, return_exceptions=True)

    type_counts = Counter(type(r) for r in responses)
    c_success, c_fail = type_counts[dict], type_counts[aiohttp.ClientError]
    print(
        f"{c_success}/{len(tasks)} URL(s) processed successfully. ",
        f"{c_fail} skipped due to errors.",
    )
    # Remove failures for response processing
    responses = [r for r in responses if type(r) == dict]
    return responses


def get_tasks(
    request_urls: list[str], api_args_dict: dict[str, Any]
) -> list[Coroutine]:
    """Creates a list of tasks that call get_response() with request params."""
    tasks = []
    for url in request_urls:
        api_args_dict["url"] = url
        tasks.append(get_response(**api_args_dict))
    return tasks
