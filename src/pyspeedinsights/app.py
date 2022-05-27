import sys
import json
from argparse import ArgumentParser

from pyspeedinsights.core.api import API

def main():
    url = sys.argv[1]
    api = API(url)
    result = api.get()
    formatted_result = json.dumps(result, indent=4)
    print(formatted_result)