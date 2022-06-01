from pyspeedinsights.core.commands import parse_args
from pyspeedinsights.api.request import get_response, get_base_url_from_sitemap
from pyspeedinsights.api.response import ResponseHandler
from pyspeedinsights.core.excel import ExcelWorkbook
from pyspeedinsights.core.sitemap import request_sitemap, parse_sitemap


def main():
    arg_groups = parse_args()
    api_args_dict = vars(arg_groups['API Group'])
    proc_args_dict = vars(arg_groups['Processing Group'])
    
    # Create a new dict without None values to avoid overriding default
    # values when passed as kwargs into ResponseHandler.
    # Not needed for get_response() func (all kwargs are default None).
    proc_args_dict = {k: v for k, v in proc_args_dict.items() if v is not None}
    format = proc_args_dict.get('format')
    category = api_args_dict.get('category', 'performance')
    if category is None:
        category = 'performance'
    url = api_args_dict.get('url')
    
    if format == 'sitemap':
        sitemap_url = url
        sitemap = request_sitemap(sitemap_url)
        request_urls = parse_sitemap(sitemap)
    else:
        request_urls = [url]
    
    for i, url in enumerate(request_urls):
        # Construct URL from cmd args and make API call
        api_args_dict.setdefault('url', url)
        if format == ('sitemap'):
            api_args_dict['url'] = get_base_url_from_sitemap(url)
        response = get_response(**api_args_dict)
    
        # Process the response based on cmd args
        r_handler = ResponseHandler(response, category, **proc_args_dict)
        r_handler.execute()
        
        if format in ['excel', 'sitemap']:
            metadata = r_handler.metadata
            audit_results = r_handler.audit_results
            metrics_results = r_handler.metrics_results
            
            # Create worksheet on first iteration and update attrs after that
            is_first = i == 0
            if is_first:
                workbook = ExcelWorkbook(url, metadata, audit_results, metrics_results)
                workbook.setup_worksheet()
            else:
                workbook.url = url
                workbook.metadata = metadata
                workbook.audit_results = audit_results
                workbook.metrics_results = metrics_results
                
            workbook.write_to_worksheet(is_first)
    
    if format in ['excel', 'sitemap']:
        workbook.workbook.close()