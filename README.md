# pyspeedinsights

**Warning: Archived on 08/11/2023 due to lack of interest. Please consider alternatives such as [Unlighthouse](https://unlighthouse.dev/).**

Measure your site speed, performance, accessibility and SEO in bulk from the command line with Python and the PageSpeed Insights API.

Support for sitemap parsing and asynchronous requests with aiohttp. Outputs to JSON or a color-coded Excel sheet for further analysis.

![A screenshot of the tool's Excel output](https://raw.githubusercontent.com/wjh18/pyspeedinsights/master/images/screenshot.png)

## What is pyspeedinsights?

A simple Python cli that parses your sitemap, sends async requests to the PageSpeed Insights API and writes color-coded Lighthouse results to Excel.

## Why pyspeedinsights?

Manually running each page of your website through Google's Lighthouse or PageSpeed Insights can be extremely time consuming, especially if it has a large number of pages.

This makes it difficult to analyze its overall performance from a 10,000-foot view without manually testing many similar types of pages.

That's what this package attempts to solve. While there are similar tools out there, pyspeedinsights is the first Python implementation built to support analysis in bulk via async requests.

Its user-friendly cli gives you the ability to analyze your entire site's speed, SEO, and accessibility results quickly and uncover bottlenecks by reviewing color-coded audit results and metrics for each page in Excel.

## Format Options

The pyspeedinsights cli supports 3 overarching formats:

1. **Single page JSON (`-f json`)**: Output the raw JSON response from the API to your working directory. If you want to analyze a single page in JSON, use this.
2. **Single page Excel (`-f excel`)**: Write color-coded Lighthouse audits (any category) and/or PageSpeed CrUX metrics (performance category only) to an Excel sheet. If you want to analyze a single page in Excel, use this.
3. **Sitemap / Multi-page Excel (`-f sitemap`)**: Specify a sitemap file to parse and output your full site's color-coded Lighthouse audits (any category) and/or PageSpeed CrUX metrics (performance category only) to an Excel sheet. If you want to analyze your entire site in Excel, use this.

There are additional customizations available for request parameters and response processing via the cli as well.

Please reference the [commands](#command-line-arguments) section for further instructions on how to specify formats and customize other options from the cli.

## Installation

From a virtual environment:

```shell
pip install pyspeedinsights
```

From a system Python3 install on MacOS:

```shell
python3 -m pip install pyspeedinsights
```

From a system Python3 install on Windows:

```shell
py -m pip install pyspeedinsights
```

To run the package as a module without installing it from PyPI, clone or download it, `cd` into the `src` directory and run:

```shell
python -m pyspeedinsights
```

*Note that your PATH, OS or Python version may require that you modify these commands slightly. When in doubt, just install it like you would any other Python package.*

## Authorization

The PageSpeed Insights API requires users to generate an API key for anything beyond running basic test requests. Otherwise, you'll hit a rate limit rather quickly.

For this reason, a valid API key is currently required to use this package. Please see the [PageSpeed Insights API documentation](https://developers.google.com/speed/docs/insights/v5/get-started) for detailed instructions on how to generate a key.

### Keys & Quotas

The key itself is added to the GET request URL as a query parameter.

It's recommended to generate the key in *Google Cloud Console > Credentials* then restrict it to your host and the PageSpeed Insights API service. If you do go this route, make sure to enable the service in *Enabled APIs & Services*, as it may not be enabled by default.

The API has a daily and per-minute request quota of 25,000 and 240, respectively. To comply with this, the package automatically sleeps requests for 1 second between each call to avoid hitting the per minute quota or overloading the API and getting hit with 500 errors.

### Keyring

This package uses the `keyring` Python library to store API keys securely on your system's default keystore (e.g. MacOS Keychain for MacOS users).

*Note: If you're unable to use keyring for whatever reason, a fallback input will prompt you for your API key from the command line at the start of each run.*

The dependency is installed automatically when you `pip install pyspeedinsights`. If for whatever reason you're getting a `ImportError: No module named keyring` error, run `pip install keyring` before running any `keyring` operations.

Please see the [`keyring` documentation](https://github.com/jaraco/keyring#command-line-utility) if you require any additional help with the following commands.

### Saving Your API Key

To save your API key to your default keystore, run:

```shell
keyring set system psikey
```

The last argument has to be `psikey`. This is because `pyspeedinsights` looks for that username to read in your key during requests. `system` will instruct `keyring` to automatically detect your system's default keystore.

You'll then receive a prompt where you can enter your key to save it.

### Verifying Your API Key

To verify that your key can be read, run:

```shell
keyring get system psikey
```

Your key should be output to the command line.

### Removing Your API Key

To remove your API key from your default keystore, run:

```shell
keyring del system psikey
```

Then verify that it's no longer accessible with `keyring get system psikey`.

## Sitemap Support

Currently, only URLs to valid XML sitemaps are supported for reports that utilize sitemap format. Please see [sitemaps.org](https://sitemaps.org/protocol.html) for specification details. Gzipped sitemap (e.g. `sitemap.xml.gz`) support is on the near-term roadmap.

Your web server or sitemap plugin must also allow robots to crawl your sitemap. If you see any permission errors that would be the first thing to check. Certain security solutions like CloudFlare also block crawlers so whitelisting the server you're running the package from may also be preferrable.

Your sitemap URL should be passed in as the positional argument for `url` when running `psi` from the command line.

### Sitemap Index

Support for sitemap index detection is also supported. This requires no additional action on your part. Simply pass your sitemap index in as the `url` argument via the cli.

If a sitemap index is detected, the package will recursively gather the URLs listed in each sitemap in your sitemap index and include them in requests. If a standard sitemap file is passed, only the URLs in that sitemap will be processed.

## Command Line Arguments

If you've installed `pyspeedinsights` with `pip`, the default command to run cli commands is `psi`.

If you've simply cloned or downloaded the repo, you can run the cli as a module directly with `python -m pyspeedinsights`. Make sure to `cd` into the `src` directory first.

For help with the following commands, run `psi --help` or `psi -h`.

### Notable Defaults

- `category` - `performance`
- `strategy`- `desktop`
- `locale` - `en` (US English)

### Quickstart

To get you started quickly, here are a few example commands.

Example of requesting a desktop performance report for all the URLs in your sitemap:

- `psi https://example.com/sitemap.xml -f sitemap -c performance -s desktop -l en`
  - Equivalent to: `psi https://example.com/sitemap.xml -f sitemap`

Example of the same report but also specifying a UTM campaign name/source and captcha token:

- `psi https://example.com/sitemap.xml -f sitemap -uc my-campaign-name -us my-campaign-source -t my-captcha-token`

### Request / Sitemap URL: `url` (required)

The URL of the page you want to analyze *or* a path to a valid XML sitemap/index if sitemap format was selected.

This must be a fully qualified url with an optional path. URLs without a scheme default to `https`. URL fragments (`#`) and query parameters (`?`) will be removed automatically.

Some valid commands:

- `psi https://example.com`
- `psi https://www.example.com`
- `psi https://example.com/test`
- `psi example.com`
  - Modified URL: `https://example.com`
- `psi https://example.com#test`
  - Modified URL: `https://example.com`

Some invalid commands:

- `psi example`
  - Throws an error
- `psi example/path`
  - Throws an error

Sitemap example:

- `psi https://example.com/sitemap.xml -f sitemap`
  - Parses `sitemap.xml` and prepares requests for all `<loc>` elements.

Please see [sitemaps](#sitemap-support) for more info.

### Output Format: `-f` or `--format` (optional)

The format of the Lighthouse results output.

- `json` (default): Output the raw JSON response from the API to your working directory (single pages only). You can add a `-f json` argument explicitly or leave it out to simply default to JSON output.

- `excel`: Write color-coded Lighthouse audits (any category) and/or PageSpeed CrUX metrics (performance category only) to an Excel sheet (analyze the single `url` only).

- `sitemap`: Specify a sitemap (or index) file to parse and output your full site's color-coded Lighthouse audits (any category) and/or PageSpeed CrUX metrics (performance category only) to an Excel sheet. When using this option, the `url` argument above needs to be a direct link to your XML sitemap/index. Please see [sitemaps](#sitemap-support) for more info.

Example:

- `psi https://example.com` - defaults to `json`
- `psi https://example.com -f json`
- `psi https://example.com -f excel`
- `psi https://example.com -f sitemap`

### Metrics: `-m` or `--metrics` (optional)

Deprecated in favor of automatically including CrUX metrics if they are available and `performance` category is selected. The previous metrics were debug metrics and subject to change by Google at any time, which made package maintenance difficult.

The new metrics include user-friendly scores instead of raw performance metrics to help give you a quick overview of core metrics like CLS, LCP, etc.

### Category: `-c` or `--category` (optional)

The Lighthouse category to run. Defaults to `performance`.

Other options include `accessibility`, `best-practices`, `pwa` and `seo`.

Metrics will only be included with the `performance` category.

Example:

- `psi https://example.com -c accessibility`

### Strategy: `-s` or `--strategy` (optional)

The Lighthouse analysis strategy to use. Defaults to `desktop`.

Other options include `mobile`.

Example:

- `psi https://example.com -s mobile`

### Locale: `-l` or `--locale` (optional)

The locale used to localize formatted results (language). Defaults to `en` (US).

Please see the PSI API docs for a [full list of locale options](https://developers.google.com/speed/docs/insights/languages).

Example:

- `psi https://example.com -l fr` - localize results to French

### UTM Campaign: `-uc` or `--campaign` (optional)

The UTM campaign name for analytics. Defaults to `None`.

This will add a query parameter to the request made by the PageSpeed Insights API (`?utm_campaign=audit`) so you can differentiate this traffic from real user traffic in Google Analytics.

Pass in the name of your campaign, `audit` is just an example.

Example:

- `psi https://example.com -uc audit`

### UTM Source: `-us` or `--source` (optional)

The UTM campaign source for analytics. Defaults to `None`.

This will add a query parameter to the request made by the PageSpeed Insights API (`?utm_source=psi`) so you can differentiate this traffic from real user traffic in Google Analytics.

Feel free to customize the name of the source, `psi` is just an example.

Example:

- `psi https://example.com -us psi`

### Captcha Token: `-t` or `--token` (optional)

The captcha token passed when filling out a captcha. Defaults to `None`.

This will add a query parameter to the request made by the PageSpeed Insights API (`?utm_source=psi`) containing your captcha token. If you have captcha protection enabled on your site, passing this token as an argument to bypass it will ensure that PSI can analyze your site.

Example:

- `psi https://example.com -t my-captcha-token`

## Help

Please open an issue on GitHub if you run into any issues or need assistance.

## Contributing

Contributors of all skill levels are welcome to help improve this package. Please see the [Contribution Guidelines](CONTRIBUTING.md) for details.
