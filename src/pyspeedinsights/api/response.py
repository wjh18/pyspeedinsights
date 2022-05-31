import json

from ..conf.settings import SITEMAP_URL
from ..conf.data import COMMAND_CHOICES


class ResponseHandler:
    def __init__(self, response, category=None, format="json", page_limit=None,
                 audits=None, metrics=None):
        self.response = response
        self.category = category
        self.format = format        
        self.page_limit = page_limit
        self.audits = audits
        self.metrics = metrics
        self.audit_results = {}
        self.metrics_results = {}
    
    @staticmethod
    def _get_sitemap_url():
        return SITEMAP_URL
    
    def _to_format(self):
        json_resp = self.response.json()
        
        if self.format == "json":
            self._process_json(json_resp)
        elif self.format == "excel":
            self._process_excel(json_resp)
            
    def _process_json(self, json_resp):
        """
        _dump_json() is likely sufficient for now, but if any other json
        operations are needed in the future, this class will be able to call
        all of them while maintaining a separation of concerns between methods.
        """
        return self._dump_json(json_resp)
    
    def _process_excel(self, json_resp):
        audits_base = self._get_audits_base(json_resp)
        self.audit_results = self._parse_audits(audits_base)
        
        has_metrics = self.metrics is not None
        is_perf = self.category == 'performance' or self.category is None
        if has_metrics and is_perf:
            self.metrics_results = self._parse_metrics(audits_base)        
            
    def _dump_json(self, json_resp):
        # Dump raw json to a file
        with open('psi.json', 'w', encoding='utf-8') as f:
            json.dump(json_resp, f, ensure_ascii=False, indent=4)
        
    def _parse_audits(self, audits_base):
        results = {}
        audits = audits_base
        for k in audits.keys():
            if audits[k].get('score') is not None:
                score = audits[k].get('score')
                num_value = audits[k].get('numericValue', 'n/a')
                results[k] = [score*100, num_value]
            
        return results
    
    def _parse_metrics(self, audits_base):
        results = {}
        metrics = audits_base["metrics"]["details"]["items"][0]
        if "all" in self.metrics:
            metrics_to_use = COMMAND_CHOICES['metrics']
            metrics_to_use.remove('all')
        else:
            metrics_to_use = self.metrics
        for field in metrics_to_use:
            metric = metrics[field]
            results[field] = metric
        return results
    
    @staticmethod
    def _get_audits_base(json_resp):
        return json_resp["lighthouseResult"]["audits"]
    
    def execute(self):
        return self._to_format()