from pyspeedinsights.core.parser import parse_args
from pyspeedinsights.core.api import API


def main():
    args = parse_args()
    args_dict = vars(args)
    api = API(**args_dict)
    api.get_data()