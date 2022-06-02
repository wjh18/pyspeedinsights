import aiohttp
import asyncio
from urllib.parse import urlsplit

import keyring


async def get_response(url, session, category=None, locale=None, strategy=None, 
             utm_campaign=None, utm_source=None, captcha_token=None):
    """
    Make async calls to PSI API for each site URL and return the response.
    """
    
    url = validate_url(url)
    params = {
        'url': url, 'category': category, 'locale': locale,
        'strategy': strategy, 'utm_campaign': utm_campaign,
        'utm_source': utm_source, 'captcha_token': captcha_token
    }
    params = {k: v for k, v in params.items() if v is not None}
    base_url = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"
    
    PSI_API_KEY = keyring.get_password("system", "psikey")
    if PSI_API_KEY is not None:
        params['key'] = PSI_API_KEY
    else:
        err = "Error: Your PageSpeed Insights API key is empty.\
              \nGenerate a key with Google and set it with the command `keyring set system psikey`.\
              \nTo verify your key can be found, run the command `keyring get system psikey`."
        raise SystemExit(err)
    
    try:
        print("Making request...")
        resp = await session.get(url=base_url, params=params)              
        resp.raise_for_status()
        print("Request successful!")
    except aiohttp.ClientConnectionError as err_cc:
        raise SystemExit(err_cc)
    except aiohttp.ClientError as err_c:
        raise SystemExit(err_c)
    
    resp = await resp.json()
    
    return resp


async def gather_responses(request_urls, api_args_dict):
    """
    Gather tasks and await the return of the responses for processing.
    """
    async with aiohttp.ClientSession() as session:
        tasks = get_tasks(request_urls, session, api_args_dict)
        responses = await asyncio.gather(*tasks)
    return responses


def get_tasks(request_urls, session, api_args_dict):
    """
    Create a list of tasks that call get_response() with request params.
    """
    tasks = []
    for url in request_urls:
        api_args_dict['url'] = url
        api_args_dict.setdefault('session', session)
        tasks.append(get_response(**api_args_dict))
    return tasks


def validate_url(url):
    """
    Adds a scheme to the URL if missing.
    Validates that the URL is fully qualified and not just a path.
    """
    err = "Invalid URL. Please enter a valid Fully-Qualified Domain Name (FQDN)."
    try:
        u = urlsplit(url)
        if not (u.scheme and u.netloc):
            if "." not in u.path:
                raise SystemError(err)
            u = u._replace(scheme='https', netloc=u.path, path='')
        return u.geturl()
    except:
        raise SystemExit(err)
