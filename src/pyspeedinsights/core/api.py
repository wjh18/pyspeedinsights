import requests

from ..conf import settings


class API:
    base_url = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"
    
    def __init__(self, url, category="performance", locale="en-US", strategy="desktop", 
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
    
    @staticmethod
    def _get_sitemap_url():
        return settings.SITEMAP_URL
    
    def _get_params(self):
        return vars(self)
    
    def get(self):
        params = self._get_params()
        params['key'] = self._get_api_key()
        r = requests.get(self.base_url, params=params)
        response = r.json()
        return response