from pprint import pprint

from pyspeedinsights.core.commands import parse_args
from pyspeedinsights.api.request import get_response
from pyspeedinsights.api.response import ResponseHandler
from pyspeedinsights.core.excel import ExcelWorkbook


def main():
    arg_groups = parse_args()
    api_args_dict = vars(arg_groups['API Group'])
    proc_args_dict = vars(arg_groups['Processing Group'])
    
    # Create a new dict without None values to avoid overriding default
    # values when passed as kwargs into ResponseHandler.
    # Not needed for get_response() func (all kwargs are default None).
    proc_args_dict = {k: v for k, v in proc_args_dict.items() if v is not None}
    
    # Construct URL from cmd args and make API call
    response = get_response(**api_args_dict)
    
    # Process the response based on cmd args
    r_handler = ResponseHandler(response, **proc_args_dict)
    r_handler.execute()
    
    # Print the results (temporary verification)
    pprint(r_handler.audit_results)
    pprint(r_handler.metrics_results)
    
    if proc_args_dict.get('results') == 'excel':
        audit_results = r_handler.audit_results
        metrics_results = r_handler.metrics_results
        
        # Create worksheet and write results to it
        url = api_args_dict['url']
        workbook = ExcelWorkbook(url, audit_results, metrics_results)
        workbook.setup_worksheet()
        workbook.write_to_worksheet()