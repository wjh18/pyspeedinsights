import requests

from ..conf import settings


class API:
    base_url = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"
    
    def __init__(self, url, category=None, locale=None, strategy=None, 
                 utm_campaign=None, utm_source=None, captcha_token=None):
        self.url = url       
        self.category = category
        self.locale = locale
        self.strategy = strategy
        self.utm_campaign = utm_campaign
        self.utm_source = utm_source
        self.captcha_token = captcha_token
    
    @staticmethod
    def _get_api_key():
        return settings.PSI_API_KEY
    
    def _get_params(self):
        return vars(self)
    
    def get_data(self):
        params = self._get_params()
        params['key'] = self._get_api_key()
        resp = requests.get(self.base_url, params=params)
        # print(resp.url)
        return resp