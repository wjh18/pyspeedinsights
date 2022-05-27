import json

from ..conf import settings


class Process:
    def __init__(self, response, format="json"):
        self.response = response
        self.format = format
    
    @staticmethod
    def _get_sitemap_url():
        return settings.SITEMAP_URL
    
    def _to_format(self):
        if self.format == "json":
            self._dump_json(self.response)
        else:
            # Placeholder for excel processing
            print('Excel')
            
    def _dump_json(self, response):
        json_resp = response.json()
        # Dump raw json to a file
        with open('psi.json', 'w', encoding='utf-8') as f:
            json.dump(json_resp, f, ensure_ascii=False, indent=4)
            
    def execute(self):
        return self._to_format()