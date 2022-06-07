import asyncio

from .api.request import gather_responses
from .api.response import process_excel, process_json
from .cli import commands
from .core.excel import ExcelWorkbook
from .core.sitemap import parse_sitemap, request_sitemap


def main():
    """
    Main execution loop of the program.

    Run with `psi` console script entry point or when invoking the module directly.
    """
    # Set up arg parser and parse cmd line args into groups.
    parser = commands.set_up_arg_parser()
    args = commands.parse_args(parser)
    arg_groups = commands.create_arg_groups(parser, args)

    # Convert arg groups to dicts.
    api_args_dict = vars(arg_groups["API Group"])
    proc_args_dict = vars(arg_groups["Processing Group"])

    # Remove keys with None values to avoid overriding kwargs.
    proc_args_dict = {k: v for k, v in proc_args_dict.items() if v is not None}

    format = proc_args_dict.get("format")
    metrics = proc_args_dict.get("metrics")

    url = api_args_dict.get("url")
    category = api_args_dict.get("category")
    strategy = api_args_dict.get("strategy")

    # API's default category and strategy with no query params.
    if category is None:
        category = "performance"
    if strategy is None:
        strategy = "desktop"

    if format == "sitemap":
        # Create list of request URLs based on sitemap.
        sitemap_url = url
        sitemap = request_sitemap(sitemap_url)
        request_urls = parse_sitemap(sitemap)
        request_urls = list(set(request_urls))  # Remove duplicates if they exist.
    else:
        # For analyzing a single page, only process the requested URL.
        request_urls = [url]

    # Make async requests to PSI API and gather responses.
    responses = asyncio.run(gather_responses(request_urls, api_args_dict))

    json_output = format == "json" or format is None
    excel_output = format in ["excel", "sitemap"]

    # Process and write data for each response based on chosen format.
    for i, response in enumerate(responses):

        if json_output:
            # Output raw JSON response to the current directory.
            process_json(response, category, strategy)

        elif excel_output:
            # Parse metadata, audit and metrics results for Excel.
            excel_results = process_excel(response, category, metrics)

            metadata = excel_results["metadata"]
            audit_results = excel_results["audit_results"]
            metrics_results = excel_results["metrics_results"]
            final_url = response["lighthouseResult"]["finalUrl"]

            is_first = i == 0
            if is_first:
                # Create and set up the workbook on the first iteration.
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

            # Write the results to the Excel worksheet.
            workbook.write_to_worksheet(is_first)

        else:
            raise ValueError("Invalid format specified. Please try again.")

    if excel_output:
        # Calculate the avg score, close the workbook and save the Excel file.
        workbook.finalize_and_save()
