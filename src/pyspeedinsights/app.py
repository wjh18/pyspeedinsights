from pyspeedinsights.core.parser import parse_args
from pyspeedinsights.core.api import API
from pyspeedinsights.core.process import Process


def main():
    arg_groups = parse_args()
    api_args_dict = vars(arg_groups['API Group'])
    proc_args_dict = vars(arg_groups['Processing Group'])
    
    # Create a new dict without None values to avoid overriding default
    # values when passed as kwargs into the Process class.
    # Not needed for api_args_dict (API class defaults are all None).
    proc_args_dict = {k: v for k, v in proc_args_dict.items() if v is not None}
    
    # Construct URL from cmd args and make API call
    api = API(**api_args_dict)
    response = api.get_data()
    
    # Process the response based on cmd args
    process = Process(response, **proc_args_dict)
    process.execute()