from .api.request import run_requests
from .api.response import process_excel, process_json
from .cli.commands import (
    arg_group_to_dict,
    create_arg_groups,
    parse_args,
    set_up_arg_parser,
)
from .core.excel import ExcelWorkbook
from .core.sitemap import process_sitemap, request_sitemap
from .utils.generic import remove_dupes_from_list, remove_nonetype_dict_items


def main() -> None:
    """Runs the main execution loop of the program.

    Called with `psi` command in cli or via invoking the module directly.
    """
    parser = set_up_arg_parser()
    args = parse_args(parser)
    arg_groups = create_arg_groups(parser, args)
    api_args_dict = arg_group_to_dict(arg_groups, "API Group")
    proc_args_dict = arg_group_to_dict(arg_groups, "Processing Group")

    # Avoid overriding kwargs by removing items with NoneType values
    proc_args_dict = remove_nonetype_dict_items(proc_args_dict)

    format = proc_args_dict.get("format")
    metrics = proc_args_dict.get("metrics")

    url = api_args_dict.get("url")
    category = api_args_dict.get("category")
    strategy = api_args_dict.get("strategy")

    # API's default category and strategy with no query params.
    category = "performance" if category is None else category
    strategy = "desktop" if strategy is None else strategy

    if format == "sitemap":
        sitemap = request_sitemap(url)
        request_urls = remove_dupes_from_list(process_sitemap(sitemap))
    else:
        request_urls = [url]  # Only request a single page's URL

    responses = run_requests(request_urls, api_args_dict)

    json_output = format == "json" or format is None
    excel_output = format in ["excel", "sitemap"]

    for num, response in enumerate(responses):
        if json_output:
            process_json(response, category, strategy)
        elif excel_output:
            excel_results = process_excel(response, category, metrics)

            metadata = excel_results["metadata"]
            audit_results = excel_results["audit_results"]
            metrics_results = excel_results["metrics_results"]
            final_url = response["lighthouseResult"]["finalUrl"]

            first_resp = num == 0
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
