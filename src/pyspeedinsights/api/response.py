import json

from ..conf import settings


default_fields = {
    'speed-index', 'first-contentful-paint',                         
    'largest-contentful-paint', 'max-potential-fid',                         
    'cumulative-layout-shift'
}


class ResponseHandler:
    def __init__(self, response, format="json", page_limit=None,
                 fields=default_fields):
        self.response = response
        self.format = format        
        self.page_limit = page_limit
        self.fields = fields
        self.results = {}
    
    @staticmethod
    def _get_sitemap_url():
        return settings.SITEMAP_URL
    
    def _to_format(self):
        if self.format == "json":
            self._process_json(self.response)
        elif self.format == "excel":
            self._process_excel(self.response)
            
    def _process_json(self, response):
        """
        _dump_json() is likely sufficient for now, but if any other json
        operations are needed in the future, this class will be able to call
        all of them while maintaining a separation of concerns between methods.
        """
        return self._dump_json(response)    
            
    def _dump_json(self, response):
        json_resp = response.json()
        # Dump raw json to a file
        with open('psi.json', 'w', encoding='utf-8') as f:
            json.dump(json_resp, f, ensure_ascii=False, indent=4)
            
    def _process_excel(self, response):
        self.results = self._parse_fields(response)
        
    def _parse_fields(self, response):
        json_resp = response.json()
        results = {}
        for field in self.fields:
            audit = json_resp["lighthouseResult"]["audits"][field]
            score = audit["score"]
            num_value = audit["numericValue"]
            results[field] = [score, num_value]
        return results
            
    def execute(self):
        return self._to_format()