# PySpeedInsights

A simple Python wrapper for the PageSpeed Insights API.

Output results for a single URL to a `.json` file or specify a sitemap file to output your full site's Lighthouse results to an `.xlsx` workbook.

## Installation

`pip install pyspeedinsights`

## Authorization

The PageSpeed Insights API requires you to generate an API key for anything more than simple testing. Otherwise, you'll hit a rate limit rather quickly.

For this reason, a valid API key is currently required to use this package. Please see the [PageSpeed Insights API documentation](https://developers.google.com/speed/docs/insights/v5/get-started) for instructions on how to generate a key.

### Keyring

This package uses the `keyring` Python library to store API keys securely on your system's default keystore (e.g. MacOS Keychain for MacOS users).

This dependency is installed automatically when you `pip install pyspeedinsights`. If not, run `pip install keyring` before running any `keyring` operations.

Please see the [`keyring` documentation](https://github.com/jaraco/keyring#command-line-utility) for help with the following commands.

### Saving Your API Key

To save your API key to your default keystore, run `keyring set system psikey`.

The last argument needs to be `psikey` because `pyspeedinsights` looks for that username to read in your key during requests. `system` will instruct `keyring` to automatically detect your system's default keystore.

You'll then receive a prompt where you can enter your key to save it.

### Verifying Your API Key

To verify that your key can be read, run `keyring get system psikey`. Your key should be output in the command line.

### Removing Your API Key

To remove your API key from your default keystore, run `keyring del system psikey`, then verify that it's no longer accessible with `keyring get system psikey`.

## Commands

If you've installed `pyspeedinsights` with `pip`, the default command to run reports is `psi`. For help with commands, run `psi --help`.

### `url` (required)

The URL of the page or site you want to analyze. This must be a fully qualified domain name with an optional path. URLs without a scheme default to `https`. URL fragments (`#`) will be removed automatically.

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

### `-f` or `--format` (optional)

The format of the results. Specify `json` (default) or `excel`.

Example:

* `psi https://example.com -f excel`

### `-m` or `--metrics` (optional)

Specify which metric(s) you want to include in your report. This only works for Excel because the json output will include everything.

If excluded, additional metrics will not be dumped to Excel. Add the `all` argument to retrieve all available metrics.

Example:

* `psi https://example.com -f excel -m all` - no additional metrics
* `psi https://example.com -f excel -m all` - all available metrics
* `psi https://example.com -f excel -m speedIndex` - just speedIndex
* `psi https://example.com -f excel -m speedIndex totalBlockingTime` - just speedIndex and totalBlockingTime

### Other commands

Further documentation will be added for request query parameter commands soon.
