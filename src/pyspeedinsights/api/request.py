import requests

from ..conf import settings
    

def get_response(url, category=None, locale=None, strategy=None, 
             utm_campaign=None, utm_source=None, captcha_token=None):
    params = {
        'url': url, 'category': category, 'locale': locale,
        'strategy': strategy, 'utm_campaign': utm_campaign,
        'utm_source': utm_source, 'captcha_token': captcha_token
    }
    base_url = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"
    
    if settings.PSI_API_KEY is not None:
        params['key'] = settings.PSI_API_KEY
    else:
        raise TypeError("""Your PageSpeed Insights API key is empty. 
                        Please generate and save a key, then try again.""")
    
    resp = requests.get(base_url, params=params)
    
    return resp