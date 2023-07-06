import logging
import ssl
import sys

from keyring.errors import KeyringError

from .api.request import run_requests
from .api.response import process_excel, process_json
from .cli.commands import arg_group_to_dict, create_arg_groups, set_up_arg_parser
from .core.excel import ExcelWorkbook
from .core.sitemap import (
    SitemapError,
    process_sitemap,
    request_sitemap,
    validate_sitemap_url,
)
from .utils.generic import remove_dupes_from_list
from .utils.urls import InvalidURLError


def main() -> None:
    """Point of execution with `psi` from cli or via direct module invocation.

    Parses cli arguments into separate groups for API calls and response processing.
    Gets request urls from sitemap or mulitple sitemaps via sitemap index.
    Prepares async API calls, awaits and returns their responses.
    Iterates through each response and writes them to the chosen format.
    """
    logging.basicConfig(
        level=logging.INFO,
        style="{",
        format="[{asctime}] {levelname:^8s} --- {message} ({filename}:{lineno})",
        handlers=(logging.FileHandler("psi.log"), logging.StreamHandler()),
    )
    logger = logging.getLogger(__name__)
    logger.info("---Starting---")

    parser = set_up_arg_parser()
    args = parser.parse_args()
    arg_groups = create_arg_groups(parser, args)
    api_args_dict = arg_group_to_dict(arg_groups, "API Group")
    proc_args_dict = arg_group_to_dict(arg_groups, "Processing Group")

    logger.info("Parsing CLI arguments.")

    format = proc_args_dict.get("format")

    url = api_args_dict.get("url")
    category = api_args_dict.get("category")
    strategy = api_args_dict.get("strategy")

    # API's default category and strategy with no query params.
    category = "performance" if category is None else category
    strategy = "desktop" if strategy is None else strategy

    json_output = format == "json" or format is None
    excel_output = format in ("excel", "sitemap")

    if format == "sitemap" and url is not None:
        try:
            sitemap = request_sitemap(url)
            request_urls = remove_dupes_from_list(process_sitemap(sitemap))
        # Let these exceptions bubble up from `core/sitemap.py`
        except (SitemapError, InvalidURLError) as err:
            logger.critical(err, exc_info=True)
            sys.exit(1)
    elif url is not None:
        logger.info("Sitemap format not specified. Only 1 URL to process.")
        if validate_sitemap_url(url):
            logger.critical(
                "Sitemaps can only be processed if sitemap format is specified."
            )
            sys.exit(1)
        request_urls = [url]

    try:
        responses = run_requests(request_urls, api_args_dict)
    # Let these exceptions bubble up from `api/request.py`
    except (
        KeyringError,
        InvalidURLError,
        OSError,
        ssl.SSLError,
        ssl.CertificateError,
    ) as err:
        logger.critical(err, exc_info=True)
        sys.exit(1)

    logger.info("Processing response data.")

    resp_num = 1  # use instead of enumerate for more control over skipping failures
    for response in responses:
        if json_output:
            logger.info("JSON format selected. Processing JSON.")
            process_json(response, category, strategy)
        elif excel_output:
            excel_results = process_excel(response, category)

            try:
                final_url = response["lighthouseResult"]["finalUrl"]
            except KeyError as err:
                # For now, log this as critical and exit.
                # A better solution would be to preserve the original request URL
                # as a fallback. Temporarily, this is more helpful than just KeyError.
                logger.critical(
                    f"The response data contains no URL: {err}", exc_info=True
                )
                sys.exit(1)

            if not excel_results:
                # Empty results from process_excel() means skip due to processing issue.
                # Don't increment resp_num here in case error occurs on first response
                # (would result in the workbook not existing for subsequent responses).
                logger.warning(
                    f"Skipping Excel processing for {final_url} due to malformed JSON."
                )
                continue

            metadata = excel_results.get("metadata")
            audit_results = excel_results.get("audit_results")
            metrics_results = excel_results.get("metrics_results")

            first_resp = resp_num == 1
            if metadata is not None and audit_results is not None:
                if first_resp:
                    logger.info("Excel format selected. Creating Excel workbook.")
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
                    logger.info("Updating workbook to process next URL.")

                workbook.write_to_worksheet(first_resp)
                resp_num += 1
        else:
            f_err = "Invalid report format specified. Please try again."
            logger.critical(f_err)
            sys.exit(1)

    if excel_output:
        workbook.finalize_and_save()
