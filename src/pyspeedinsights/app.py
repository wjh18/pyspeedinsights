from .api.request import run_requests
from .api.response import process_excel, process_json
from .cli.commands import arg_group_to_dict, create_arg_groups, set_up_arg_parser
from .core.excel import ExcelWorkbook
from .core.sitemap import process_sitemap, request_sitemap
from .utils.generic import remove_dupes_from_list


def main() -> None:
    """Point of execution with `psi` from cli or via direct module invocation.

    Parses cli arguments into separate groups for API calls and response processing.
    Gets request urls from sitemap or mulitple sitemaps via sitemap index.
    Prepares async API calls, awaits and returns their responses.
    Iterates through each response and writes them to the chosen format.
    """
    parser = set_up_arg_parser()
    args = parser.parse_args()
    arg_groups = create_arg_groups(parser, args)
    api_args_dict = arg_group_to_dict(arg_groups, "API Group")
    proc_args_dict = arg_group_to_dict(arg_groups, "Processing Group")

    format = proc_args_dict.get("format")
    metrics = proc_args_dict.get("metrics")

    url = api_args_dict.get("url")
    category = api_args_dict.get("category")
    strategy = api_args_dict.get("strategy")

    # API's default category and strategy with no query params.
    category = "performance" if category is None else category
    strategy = "desktop" if strategy is None else strategy

    json_output = format == "json" or format is None
    excel_output = format in ("excel", "sitemap")

    if metrics is not None and json_output or category != "performance":
        print("Warning: metrics are only configurable for excel performance reports.")
        print("JSON performance reports will include all metrics by default.")

    if format == "sitemap" and url is not None:
        sitemap = request_sitemap(url)
        request_urls = remove_dupes_from_list(process_sitemap(sitemap))
    elif url is not None:
        request_urls = [url]  # Only request a single page's URL

    responses = run_requests(request_urls, api_args_dict)

    for num, response in enumerate(responses):
        if json_output:
            process_json(response, category, strategy)
        elif excel_output:
            excel_results = process_excel(response, category, metrics)

            final_url = response["lighthouseResult"]["finalUrl"]
            metadata = excel_results.get("metadata")
            audit_results = excel_results.get("audit_results")
            metrics_results = excel_results.get("metrics_results")

            first_resp = num == 0
            if metadata is not None and audit_results is not None:
                if first_resp:
                    print("Creating Excel workbook...")
                    workbook = ExcelWorkbook(
                        final_url, metadata, audit_results, metrics_results
                    )
                    workbook.set_up_worksheet()
                else:
                    # Simply update the workbook attrs after the first response.
                    workbook.url = final_url
                    workbook.metadata = metadata
                    workbook.audit_results = audit_results
                    workbook.metrics_results = metrics_results

                workbook.write_to_worksheet(first_resp)
        else:
            raise ValueError("Invalid format specified. Please try again.")

    if excel_output:
        workbook.finalize_and_save()
