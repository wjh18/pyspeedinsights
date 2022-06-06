import asyncio

from pyspeedinsights.cli.commands import parse_args
from pyspeedinsights.api.request import gather_responses
from pyspeedinsights.api.response import process_response
from pyspeedinsights.core.excel import ExcelWorkbook
from pyspeedinsights.core.sitemap import request_sitemap, parse_sitemap


def main():
    """
    Main execution loop.
    """
    # Parse cmd line args and convert to dicts by arg group
    arg_groups = parse_args()
    api_args_dict = vars(arg_groups['API Group'])
    proc_args_dict = vars(arg_groups['Processing Group'])
    
    # Create a new dict without None values to avoid overriding default
    # values when passed as kwargs into process_response().
    proc_args_dict = {k: v for k, v in proc_args_dict.items() if v is not None}
    
    format = proc_args_dict.get('format')
    category = api_args_dict.get('category')
    strategy = api_args_dict.get('strategy')
    
    if category is None:
        category = 'performance'
    if strategy is None:
        strategy = 'desktop'
        
    url = api_args_dict.get('url')
    
    # Create list of request URLs based on sitemap or single arg
    if format == 'sitemap':
        sitemap_url = url
        sitemap = request_sitemap(sitemap_url)
        request_urls = parse_sitemap(sitemap)
    else:
        request_urls = [url]
        
    # Run async requests and await responses    
    responses = asyncio.run(gather_responses(request_urls, api_args_dict))
    
    for i, response in enumerate(responses):
        # Process the response based on cmd args
        results = process_response(response, category, strategy, **proc_args_dict)
        
        if format in ['excel', 'sitemap']:
            metadata = results['metadata']
            audit_results = results['audit_results']
            metrics_results = results['metrics_results']
            final_url = response['lighthouseResult']['finalUrl']
            
            # Create worksheet on first iteration, simply update attrs after that
            is_first = i == 0
            if is_first:
                print("Creating Excel workbook...")
                workbook = ExcelWorkbook(final_url, metadata, audit_results, metrics_results)
                workbook.setup_worksheet()
            else:
                workbook.url = final_url
                workbook.metadata = metadata
                workbook.audit_results = audit_results
                workbook.metrics_results = metrics_results
                
            # Write results to Excel worksheet    
            workbook.write_to_worksheet(is_first)
    
    if format in ['excel', 'sitemap']:
        # Close workbook to save the Excel sheet
        workbook.finalize_and_save()