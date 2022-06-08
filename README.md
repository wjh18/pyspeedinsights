# pyspeedinsights

A simple Python cli that parses your sitemap, sends async requests to the PageSpeed Insights API and writes color-coded Lighthouse results to Excel.

![pyspeedinsights](https://github.com/wjh18/pyspeedinsights/blob/master/images/screenshot.png)

## Why pyspeedinsights?

Manually running your website's pages through Lighthouse or PageSpeed Insights can be extremely time consuming and difficult to manage. Especially with a large site.

I personally had a hard time analyzing my site's overal performance from a 10,000-foot view without manually testing many similar types of pages.

That's why I made this package. While there are similar tools out there, I couldn't find any solid Python ones that were easy to use.

The pyspeedinsights cli allows you to analyze your entire site's performance quickly and uncover bottlenecks by reviewing color-coded audit results and metrics for each page in Excel.

## Format Options

The pyspeedinsights cli supports 3 overarching formats:

1. **Single page JSON (`-f json`)**: Output the raw JSON response from the API to your working directory (single pages only).
2. **Single page Excel (`-f excel`)**: Write color-coded Lighthouse audits and (optionally) metrics to an Excel sheet (single pages only).
3. **Sitemap / Multi-page Excel (`-f sitemap`)**: Specify a sitemap file to parse and output your full site's color-coded Lighthouse audits and (optionally) metrics to an Excel sheet.

There are additional customizations available for request parameters and response processing via the cli as well.

Please reference the [commands](#command-line-arguments) section for further instructions on how to specify formats and customize other options from the cli.

## Installation

From a virtual environment:

`pip install pyspeedinsights`

From a system Python3 install on MacOS:

`python3 -m pip install pyspeedinsights`

From a system Python3 install on Windows:

`py -m pip install pyspeedinsights`

*Note that your PATH, OS or Python version may require that you modify these commands slightly. When in doubt, just install it like you would any other Python package.*

## Authorization

The PageSpeed Insights API requires users to generate an API key for anything more than simple testing. Otherwise, you'll hit a rate limit rather quickly.

For this reason, a valid API key is currently required to use this package. Please see the [PageSpeed Insights API documentation](https://developers.google.com/speed/docs/insights/v5/get-started) for detailed instructions on how to generate a key.

### Keys & Quotas

The key itself is added to the GET request URL as a query parameter.

It's recommended to generate the key in Google Cloud Console > Credentials then restrict it to your host and the PageSpeed Insights API service. If you do go this route, make sure to enable the service in Enabled APIs & Services, as it may not be enabled by default.

The API has a daily and per-minute request quota of 25,000 and 240, respectively. The async requests are slept for 1s between each call to avoid hitting the per minute quota or overloading the API and getting hit with 500 errors.

### Keyring

This package uses the `keyring` Python library to store API keys securely on your system's default keystore (e.g. MacOS Keychain for MacOS users).

This dependency is installed automatically when you `pip install pyspeedinsights`. If for some reason it's not, run `pip install keyring` before running any `keyring` operations.

Please see the [`keyring` documentation](https://github.com/jaraco/keyring#command-line-utility) if you require any additional help with the following commands.

### Saving Your API Key

To save your API key to your default keystore, run `keyring set system psikey`.

The last argument has to be `psikey`. This is because `pyspeedinsights` looks for that username to read in your key during requests. `system` will instruct `keyring` to automatically detect your system's default keystore.

You'll then receive a prompt where you can enter your key to save it.

### Verifying Your API Key

To verify that your key can be read, run `keyring get system psikey`. Your key should be output to the command line.

### Removing Your API Key

To remove your API key from your default keystore, run `keyring del system psikey`, then verify that it's no longer accessible with `keyring get system psikey`.

## Sitemap Support

Currently only valid XML sitemaps are supported for reports that use sitemap format.

Your web server or sitemap plugin must also allow robots to crawl your sitemap. If you see any permission errors that would be the first thing to check.

In the future, support for sitemap indices, multiple sitemaps and more advanced sitemap parsing will hopefully be added.

Sitemap URLs should be passed in as positional arguments for `url` when running `psi` from the command line.

## Command Line Arguments

If you've installed `pyspeedinsights` with `pip`, the default command to run cli commands is `psi`.

If you've simply cloned the repo, you can run the cli as a module directly with `python -m pyspeedinsights`.

For help with the following commands, run `psi --help`.

### Quickstart

To get you started quickly, here are a few example commands.

Example of requesting a desktop performance report with all metrics for all the URLs in your sitemap:

* `psi https://www.example.com/sitemap.xml -f sitemap -m all -c performance -s desktop -l en`
  * Equivalent to: `psi https://www.example.com/sitemap.xml -f sitemap -m all` (`performance`, `desktop` and `en` are defaults)

Example of the same report but also specifying a UTM campaign name/source and captcha token (experimental / untested):

* `psi https://www.example.com/sitemap.xml -f sitemap -m all -uc my-campaign-name -us my-campaign-source -t my-captcha-token`

### Request / Sitemap URL: `url` (required)

The URL of the page you want to analyze OR a path to a valid XML sitemap if using sitemap format.

This must be a fully qualified domain name with an optional path. URLs without a scheme default to `https`. URL fragments (`#`) will be removed automatically.

Good:

* `psi https://example.com`
* `psi https://www.example.com`
* `psi https://example.com/test`
* `psi example.com`
  * Modified URL: `https://example.com`
* `psi https://example.com#test`
  * Modified URL: `https://example.com`

Bad:

* `psi example`
  * Throws an error

Sitemap example:

* `psi https://www.example.com/sitemap.xml -f sitemap`
  * Parses `sitemap.xml` and prepares requests for all `<loc>` elements.

Please see [sitemaps](#sitemap-support) for more info.

### Output Format: `-f` or `--format` (optional)

The format of the Lighthouse results output.

**`json` (default)** - Output the raw JSON response from the API to your working directory (single pages only). You can add a `-f json` argument explicitly or leave it out to simply default to JSON output.

**`excel`** - Write color-coded Lighthouse audits and (optionally) metrics to an Excel sheet (analyze the single `url` only).

`sitemap` - Specify a sitemap file to parse and output your full site's color-coded Lighthouse audits and (optionally) metrics to an Excel sheet. When using this option, the `url` argument above needs to be a direct link to your XML sitemap. Please see [sitemaps](#sitemap-support) for more info.

Example:

* `psi https://example.com` - defaults to `json`
* `psi https://example.com -f excel`
* `psi https://example.com -f sitemap`

### Metrics: `-m` or `--metrics` (optional)

Specify which metric(s) you want to include in your report.

This is only supported for the performance category (`-c performance`) with either `excel` or `sitemap` formats because the JSON output includes everything by default and categories other than performance don't include metrics in the response.

If excluded, metrics will *not* be dumped to Excel. Add the `all` argument to retrieve all available metrics or specify individual metrics to include.

Example:

* `psi https://example.com -f excel` - no metrics
* `psi https://example.com -f excel -m all` - all available metrics
* `psi https://example.com -f excel -m speedIndex` - just speedIndex
* `psi https://example.com -f excel -m speedIndex totalBlockingTime` - just speedIndex and totalBlockingTime

Full list of available metrics:

* `observedTotalCumulativeLayoutShift`
* `observedCumulativeLayoutShift`
* `observedLargestContentfulPaintAllFrames`
* `maxPotentialFID`
* `observedSpeedIndexTs`
* `observedFirstContentfulPaintTs`
* `observedTimeOrigin`
* `observedFirstPaint`
* `observedNavigationStartTs`
* `observedLargestContentfulPaintAllFramesTs`
* `speedIndex`
* `observedFirstContentfulPaint`
* `observedLastVisualChangeTs`
* `cumulativeLayoutShiftMainFrame`
* `observedLastVisualChange`
* `cumulativeLayoutShift`
* `largestContentfulPaint`
* `observedDomContentLoaded`
* `firstContentfulPaint`
* `observedCumulativeLayoutShiftMainFrame`
* `observedFirstVisualChange`
* `observedFirstPaintTs`
* `totalCumulativeLayoutShift`
* `observedFirstMeaningfulPaint`
* `interactive`
* `observedTraceEnd`
* `observedFirstMeaningfulPaintTs`
* `totalBlockingTime`
* `observedFirstContentfulPaintAllFramesTs`
* `observedLargestContentfulPaint`
* `observedNavigationStart`
* `observedLoad`
* `observedFirstVisualChangeTs`
* `observedFirstContentfulPaintAllFrames`
* `observedTimeOriginTs`
* `observedTraceEndTs`
* `observedLoadTs`
* `observedDomContentLoadedTs`
* `observedSpeedIndex`
* `firstMeaningfulPaint`
* `observedLargestContentfulPaintTs`

### Category: `-c` or `--category` (optional)

The Lighthouse category to run. Defaults to `performance`.

Other options include `accessibility`, `best-practices`, `pwa` and `seo`.

Example:

* `psi https://www.example.com -c accessibility`

### Strategy: `-s` or `--strategy` (optional)

The Lighthouse analysis strategy to use. Defaults to `desktop`.

Other options include `mobile`.

Example:

* `psi https://www.example.com -s mobile`

### Locale: `-l` or `--locale` (optional)

The locale used to localize formatted results. Defaults to `en` (US).

Please see the PSI API docs for a [full list of locale options](https://developers.google.com/speed/docs/insights/languages).

Example:

* `psi https://www.example.com -l ru` - localize results to Russian

### UTM Campaign: `-uc` or `--campaign` (optional) (experimental)

The UTM campaign name for analytics. Defaults to `None`.

This option is currently experimental and hasn't been fully tested.

Example:

* `psi https://www.example.com -uc my-campaign-name`

### UTM Source: `-us` or `--source` (optional) (experimental)

The UTM campaign source for analytics. Defaults to `None`.

This option is currently experimental and hasn't been fully tested.

Example:

* `psi https://www.example.com -us my-campaign-source`

### Captcha Token: `-t` or `--token` (optional) (experimental)

The captcha token passed when filling out a captcha. Defaults to `None`.

This option is currently experimental and hasn't been fully tested.

Example:

* `psi https://www.example.com -t my-captcha-token`

## Contributing

Contributors of all skill levels are welcome to help improve this package. Please see the [Contribution Guidelines](CONTRIBUTING.md) for details.
