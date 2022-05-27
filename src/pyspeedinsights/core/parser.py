from argparse import ArgumentParser


def parse_args():
    """
    Parse command line arguments as parameters for the request.
    """
    parser = ArgumentParser(prog='pyspeedinsights')
    parser.add_argument(
        "url", help="The URL of the site you want to analyze.")
    parser.add_argument(
        "-c", "--category", metavar="\b", dest="category",
        choices=['accessibility', 'best-practices', 'performance', 'pwa', 'seo'],
        help="The Lighthouse category to run. Defaults to Performance.")
    parser.add_argument(
        "-l", "--locale", metavar="\b", dest="locale",
        choices=['en', 'es'], # add more later
        help="The locale used to localize formatted results. Defaults to English (US).")
    parser.add_argument(
        "-s", "--strategy", metavar="\b", dest="strategy",
        choices=['desktop', 'mobile'],
        help="The analysis strategy (desktop or mobile) to use. Defaults to desktop.")
    parser.add_argument(
        "-uc", "--campaign", metavar="\b", dest="utm_campaign",                        
        help="UTM campaign name for analytics.")
    parser.add_argument(
        "-us", "--source", metavar="\b", dest="utm_source",
        help="UTM campaign source for analytics.")
    parser.add_argument(
        "-t", "--token", metavar="\b", dest="utm_source",                    
        help="The captcha token passed when filling out a captcha.")
    # Add other options for what to parse from the response, whether to use sitemap, add to Excel, etc.
    
    args = parser.parse_args()
    return args