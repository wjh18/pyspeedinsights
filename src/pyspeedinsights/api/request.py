import asyncio

import aiohttp

from ..utils.urls import validate_url
from .keys import get_api_key

next_delay = 1  # Global for applying a 1s delay between requests


async def get_response(
    url,
    category=None,
    locale=None,
    strategy=None,
    utm_campaign=None,
    utm_source=None,
    captcha_token=None,
):
    """
    Make async GET calls to the PSI API for the requested page's URL.

    Return the awaited json response from the server.
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
    params = {k: v for k, v in params.items() if v is not None}

    params["key"] = get_api_key()

    # Add a 1s delay between calls to avoid 500 errors from server.
    global next_delay
    next_delay += 1
    await asyncio.sleep(next_delay)

    print(f"Sending request... ({params['url']})")

    # Make async call with query params to PSI API and await response.
    async with aiohttp.ClientSession() as session:
        async with session.get(url=base_url, params=params) as resp:

            # Retry on errors up to 5 times. Sleep for 1s between retries.
            json_resp = None
            retry_attempts = 5
            while json_resp is None:
                try:
                    resp.raise_for_status()
                    json_resp = await resp.json()
                    print(f"Request successful! ({params['url']})")
                except aiohttp.ClientError as err_c:
                    if retry_attempts < 1:
                        raise aiohttp.ClientError(err_c)
                    else:
                        print(err_c)
                        retry_attempts -= 1
                        await asyncio.sleep(1)

    return json_resp


async def gather_responses(request_urls, api_args_dict):
    """Gather tasks and await the return of the responses for processing."""

    tasks = get_tasks(request_urls, api_args_dict)
    print(f"Preparing {len(tasks)} URL(s)...")

    responses = await asyncio.gather(*tasks)
    print(f"{len(responses)}/{len(tasks)} URL(s) processed successfully.")

    return responses


def get_tasks(request_urls, api_args_dict):
    """Create a list of tasks that call get_response() with request params."""

    tasks = []
    for url in request_urls:
        api_args_dict["url"] = url
        tasks.append(get_response(**api_args_dict))

    return tasks
