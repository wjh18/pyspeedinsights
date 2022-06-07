import argparse

from .choices import COMMAND_CHOICES


def set_up_arg_parser():
    """
    Setup argument parser with grouped command line arguments.

    Used to define PSI API request query parameters and how responses are processed.
    """

    parser = argparse.ArgumentParser(prog="pyspeedinsights")

    # Add argument options for default API call query params.
    api_group = parser.add_argument_group("API Group")

    api_group.add_argument(
        "url", help="The URL or Sitemap URL of the site you want to analyze."
    )
    api_group.add_argument(
        "-c",
        "--category",
        metavar="\b",
        dest="category",
        choices=COMMAND_CHOICES["category"],
        help="The Lighthouse category to run:\
            accessibility, best-practices, performance (default), pwa or seo.",
    )
    api_group.add_argument(
        "-l",
        "--locale",
        metavar="\b",
        dest="locale",
        choices=COMMAND_CHOICES["locale"],
        help="The locale used to localize formatted results.\
            Defaults to English (US).",
    )
    api_group.add_argument(
        "-s",
        "--strategy",
        metavar="\b",
        dest="strategy",
        choices=COMMAND_CHOICES["strategy"],
        help="The analysis strategy to use: desktop (default) or mobile.",
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
        help="The format of the results: json (default), excel or sitemap.\
            json outputs all response data to a json file (1 URL at a time).\
            excel writes Lighthouse audits and (optionally) metrics\
                to an Excel file (1 URL at a time).\
            sitemap parses the sitemap URL you provide and\
                collects data for all your pages to Excel.",
    )
    proc_group.add_argument(
        "-m",
        "--metrics",
        metavar="\b",
        dest="metrics",
        choices=COMMAND_CHOICES["metrics"],
        nargs="+",
        help="The additional metric(s) to include in your report.\
            For Excel format only (the json output includes all metrics).\
            If excluded, only the default Lighthouse audits\
                will be saved to Excel.\
            Add the `all` argument to retrieve all available metrics.",
    )

    return parser


def parse_args(parser):
    """
    Parse user arguments from the command line.

    With `psi` console script entry point or when invoking the module directly.
    """

    args = parser.parse_args()
    return args


def create_arg_groups(parser, args):
    """
    Create separate namespaces for each arg group.

    Necessary for passing each arg group separately as kwargs.
    """

    arg_groups = {}

    for group in parser._action_groups:
        group_dict = {a.dest: getattr(args, a.dest, None) for a in group._group_actions}
        arg_groups[group.title] = argparse.Namespace(**group_dict)

    return arg_groups
