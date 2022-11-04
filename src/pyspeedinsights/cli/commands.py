"""Sets up, parses and groups command line arguments using argparse.

Typical usage example:
    parser = set_up_arg_parser()
    args = parse_args(parser)
    arg_groups = create_arg_groups(parser, args)
    arg_group_dict = arg_group_to_dict(arg_groups, "Group Name")
"""

from argparse import ArgumentParser, Namespace
from typing import Any, TypeAlias, Union

from .choices import COMMAND_CHOICES

ArgGroups: TypeAlias = dict[str, Namespace]


def set_up_arg_parser() -> ArgumentParser:
    """Sets up argument parser with grouped command line arguments.

    Commands are used in PSI API request query params and response processing.

    Returns:
        An argparse.ArgumentParser instance with 2 argument groups.
    """
    parser = ArgumentParser(prog="pyspeedinsights")

    # Add argument options for default API call query params.
    api_group = parser.add_argument_group("API Group")
    api_group.add_argument(
        "url", help="The URL or sitemap URL of the site being analyzed."
    )
    api_group.add_argument(
        "-c",
        "--category",
        metavar="\b",
        dest="category",
        choices=COMMAND_CHOICES["category"],
        help=(
            "The Lighthouse category to run: "
            "`accessibility`, `best-practices`, "
            "`performance` (default), `pwa` or `seo`."
        ),
    )
    api_group.add_argument(
        "-l",
        "--locale",
        metavar="\b",
        dest="locale",
        choices=COMMAND_CHOICES["locale"],
        help="The locale used to localize formatted results. Defaults to English (US).",
    )
    api_group.add_argument(
        "-s",
        "--strategy",
        metavar="\b",
        dest="strategy",
        choices=COMMAND_CHOICES["strategy"],
        help="The analysis strategy to use: `desktop` (default) or `mobile`.",
    )
    api_group.add_argument(
        "-uc",
        "--campaign",
        metavar="\b",
        dest="utm_campaign",
        help="The UTM campaign name for analytics.",
    )
    api_group.add_argument(
        "-us",
        "--source",
        metavar="\b",
        dest="utm_source",
        help="The UTM campaign source for analytics.",
    )
    api_group.add_argument(
        "-t",
        "--token",
        metavar="\b",
        dest="captcha_token",
        help="The captcha token passed when filling out a captcha.",
    )

    # Add other argument options for how to process the API response.
    proc_group = parser.add_argument_group("Processing Group")
    proc_group.add_argument(
        "-f",
        "--format",
        metavar="\b",
        dest="format",
        choices=COMMAND_CHOICES["format"],
        help=(
            "The format of the results: `json` (default), `excel` or `sitemap`. "
            "`json` outputs all response data to a json file (1 URL only). "
            "`excel` writes Lighthouse audits and (optionally) metrics "
            "to an Excel file (1 URL only). "
            "`sitemap` parses the sitemap URL you provide and writes Lighthouse audits "
            "and (optionally) metrics for all the pages in your sitemap to Excel."
        ),
    )
    proc_group.add_argument(
        "-m",
        "--metrics",
        metavar="\b",
        dest="metrics",
        choices=COMMAND_CHOICES["metrics"],
        nargs="+",
        help=(
            "The additional metric(s) to include in your report. "
            "For `excel` or `sitemap` formats only (`json` includes all metrics). "
            "If excluded, only the default Lighthouse audits will be written to Excel. "
            "Add the `all` argument to retrieve all available metrics."
        ),
    )
    return parser


def create_arg_groups(parser: ArgumentParser, args: Namespace) -> ArgGroups:
    """Creates separate namespaces for each arg group.

    Allows for separately passing each arg group as kwargs to a func or cls.

    Returns:
        A dict with group names as keys and argparse.Namespace instances as values.
    """
    arg_groups = {}
    for group in parser._action_groups:
        group_dict = {a.dest: getattr(args, a.dest, None) for a in group._group_actions}
        title = group.title
        if title:
            arg_groups[title] = Namespace(**group_dict)
    return arg_groups


def arg_group_to_dict(
    arg_groups: ArgGroups, arg_group_name: str
) -> dict[str, Union[Any, None]]:
    """Converts an arg group Namespace to a dict.

    Returns:
        A dict with str-based API or reponse processing param names as keys
        and str or NoneType as values.
    """
    return vars(arg_groups[arg_group_name])
