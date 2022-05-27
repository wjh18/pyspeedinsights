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
    params['key'] = settings.PSI_API_KEY
    resp = requests.get(base_url, params=params)
    
    return resp