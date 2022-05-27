import requests
import json

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
    
    @staticmethod
    def _get_sitemap_url():
        return settings.SITEMAP_URL
    
    def _get_params(self):
        return vars(self)
    
    def _to_format(self, response, format):
        if format == "json":
            self._dump_json(response)
            
    def _dump_json(self, response):
        json_resp = response.json()
        with open('psi.json', 'w', encoding='utf-8') as f:
            json.dump(json_resp, f, ensure_ascii=False, indent=4)
    
    def get_data(self, format="json"):
        params = self._get_params()
        params['key'] = self._get_api_key()
        r = requests.get(self.base_url, params=params)
        return self._to_format(r, format)