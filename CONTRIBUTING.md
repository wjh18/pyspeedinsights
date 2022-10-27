# Contributing

For any proposed changes or bug reports, please [open an issue](https://github.com/wjh18/pyspeedinsights/issues) first using one of the issue templates. Then feel free to work on it. You're also welcome to tackle any existing issues.

## How to contribute

* Fork the project on Github
* Clone the fork to your local machine
* Create a descriptive branch for the changes
* Make and commit your changes to the new branch
* Push your changes to the branch
* Submit a pull request on Github using the [pull request template](https://github.com/wjh18/pyspeedinsights/blob/master/.github/pull_request_template.md).

## Requirements

Requirements for development are managed by pip and pip-tools. To install them, create a virtual environment and run `pip install -r requirements.txt`.

To update requirements, add the new requirement to `requirements.in` and run `pip-compile requirements.in`, then install them with pip as shown above.

## Editable mode

It's recommended to install the package in editable mode with `pip install -e .` when testing the package in development. This will allow you to run commands with the `psi` entrypoint from your virtual environment instead of changing to the `src` directory and running the program as a module directly with `python -m pyspeedinsights`.
