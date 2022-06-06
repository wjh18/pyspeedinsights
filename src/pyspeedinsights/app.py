import asyncio

from .api.request import gather_responses
from .api.response import process_json, process_excel
from .cli import commands
from .core.excel import ExcelWorkbook
from .core.sitemap import request_sitemap, parse_sitemap


def main():
    """
    Main entry point when initialized from the cmd line with `psi`.
    """
    # Setup / parse cmd line args into groups.
    parser = commands.setup_arg_parser()
    args = commands.parse_args(parser)
    arg_groups = commands.create_arg_groups(parser, args)
    
    # Convert arg groups to dicts.
    api_args_dict = vars(arg_groups['API Group'])
    proc_args_dict = vars(arg_groups['Processing Group'])
    
    # Remove keys with None values to avoid overriding kwargs.
    proc_args_dict = {k: v for k, v in proc_args_dict.items() if v is not None}
    
    format = proc_args_dict.get('format')
    metrics = proc_args_dict.get('metrics')
    
    url = api_args_dict.get('url')
    category = api_args_dict.get('category')
    strategy = api_args_dict.get('strategy')
    
    # API's default category and strategy with no query params.
    if category is None:
        category = 'performance'
    if strategy is None:
        strategy = 'desktop'    
        
    if format == 'sitemap':
        # Create list of request URLs based on sitemap.
        sitemap_url = url
        sitemap = request_sitemap(sitemap_url)
        request_urls = parse_sitemap(sitemap)
    else:
        # For single page, only process that 1 URL.
        request_urls = [url]
        
    # Run async requests and await responses    
    responses = asyncio.run(gather_responses(request_urls, api_args_dict))
    
    json_output =  format == "json" or format is None
    excel_output = format in ['excel', 'sitemap']
    
    # Iterate through responses and write data to Excel.
    for i, response in enumerate(responses):
        
        if json_output:
            # Output raw JSON response to working directory.
            process_json(response, category, strategy)
            
        elif excel_output:
            # Parse metadata, audit and metrics results for Excel.
            excel_results = process_excel(response, category, metrics)
            
            metadata = excel_results['metadata']
            audit_results = excel_results['audit_results']
            metrics_results = excel_results['metrics_results']
            final_url = response['lighthouseResult']['finalUrl']
            
            is_first = i == 0
            if is_first:
                # Create and set up workbook on first iteration.
                print("Creating Excel workbook...")
                workbook = ExcelWorkbook(
                    final_url, metadata, audit_results, metrics_results)
                workbook.setup_worksheet()
            else:
                # Simply update workbook attrs after first response.
                workbook.url = final_url
                workbook.metadata = metadata
                workbook.audit_results = audit_results
                workbook.metrics_results = metrics_results
                
            # Write the results to Excel worksheet.
            workbook.write_to_worksheet(is_first)
            
        else:
            raise ValueError("Invalid format specified. Please try again.")
    
    if excel_output:
        # Calculate avg score, close the workbook and save to Excel.
        workbook.finalize_and_save()