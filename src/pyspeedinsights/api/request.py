import aiohttp
import asyncio
from urllib.parse import urlsplit

import keyring


next_delay = 1

async def get_response(url, category=None, locale=None, strategy=None, 
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
    
    # Get API key from keystore with keyring
    PSI_API_KEY = keyring.get_password("system", "psikey")
    if PSI_API_KEY is not None:
        params['key'] = PSI_API_KEY
    else:
        err = "Error: Your PageSpeed Insights API key is empty.\
              \nGenerate a key with Google and set it with the command `keyring set system psikey`.\
              \nTo verify your key can be found, run the command `keyring get system psikey`."
        raise SystemExit(err)
    
    # Add a delay between tasks to avoid 500 errors from server
    global next_delay
    next_delay += 1
    await asyncio.sleep(next_delay)
    
    print(f"Sending request... ({params['url']})")
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url=base_url, params=params) as resp:
    
            # Retry on errors up to 5 times
            json_resp = None
            retry_attempts = 5
            while json_resp is None:
                try:                    
                    resp.raise_for_status()         
                    json_resp = await resp.json()
                    print(f"Request successful! ({params['url']})")
                except aiohttp.ClientError as err_c:                    
                    if retry_attempts < 1:
                        raise SystemExit(err_c)
                    else:
                        print(err_c)
                        retry_attempts -= 1
                        await asyncio.sleep(1)                        
    
    return json_resp


async def gather_responses(request_urls, api_args_dict):
    """
    Gather tasks and await the return of the responses for processing.
    """
    tasks = get_tasks(request_urls, api_args_dict)
    print(f"Preparing {len(tasks)} URL(s)...")
    
    responses = await asyncio.gather(*tasks)
    print(f"{len(responses)}/{len(tasks)} URLs processed successfully.")
    
    return responses


def get_tasks(request_urls, api_args_dict):
    """
    Create a list of tasks that call get_response() with request params.
    """
    tasks = []
    for url in request_urls:
        api_args_dict['url'] = url
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
