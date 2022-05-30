import requests
import keyring
    

def get_response(url, category=None, locale=None, strategy=None, 
             utm_campaign=None, utm_source=None, captcha_token=None):
    params = {
        'url': url, 'category': category, 'locale': locale,
        'strategy': strategy, 'utm_campaign': utm_campaign,
        'utm_source': utm_source, 'captcha_token': captcha_token
    }
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
        resp = requests.get(base_url, params=params)
        resp.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        raise SystemExit(errh)
    except requests.exceptions.ConnectionError as errc:
        raise SystemExit(errc)
    except requests.exceptions.Timeout as errt:
        raise SystemExit(errt)
    except requests.exceptions.RequestException as err:
        raise SystemExit(err)
    
    return resp