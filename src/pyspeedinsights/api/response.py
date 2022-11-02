"""Response processing and parsing for PSI API results."""

import copy
import json
from datetime import datetime
from typing import Optional, Union

from ..cli.choices import COMMAND_CHOICES
from ..utils.generic import sort_dict_alpha


def process_json(json_resp: dict, category: str, strategy: str) -> None:
    """Dumps raw json response to a file in the working directory.

    Called within main() in pyspeedinsights.app.
    If json format is selected this is where program execution ends.
    """
    date = _get_timestamp(json_resp)
    filename = f"psi-s-{strategy}-c-{category}-{date}.json"

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(json_resp, f, ensure_ascii=False, indent=4)
        print("JSON processed. Check your current directory.")


def process_excel(
    json_resp: dict, category: str, metrics: Optional[list[str]]
) -> dict[str, Union[dict, None]]:
    """Calls various parsing operations for Excel / Sitemap formats.

    Called within main() in pyspeedinsights.app.
    Metrics results are only included if the category is performance.
    """
    audits_base = _get_audits_base(json_resp)  # Location of audits in json response
    metadata = _parse_metadata(json_resp, category)
    audit_results = _parse_audits(audits_base)
    if metrics is not None and category == "performance":
        metrics_results = _parse_metrics(audits_base, metrics)
    else:
        metrics_results = None

    results: dict[str, Union[dict, None]] = {
        "metadata": metadata,
        "audit_results": audit_results,
        "metrics_results": metrics_results,
    }
    return results


def _parse_metadata(json_resp: dict, category: str) -> dict[str, Union[str, int]]:
    """Parses various metadata from the JSON response to write to Excel."""
    json_base = json_resp["lighthouseResult"]
    strategy = json_base["configSettings"]["formFactor"]
    category_score = json_base["categories"][category]["score"]
    timestamp = _get_timestamp(json_resp)

    metadata = {
        "category": category,
        "category_score": category_score,
        "strategy": strategy,
        "timestamp": timestamp,
    }
    return metadata


def _parse_audits(audits_base: dict) -> dict[str, tuple[Union[int, float]]]:
    """Parses Lighthouse audits from the JSON response to write to Excel.

    Scores from 0-100 are given for the numeric value of each audit.

    Returns:
        A dict of audit results with audit names as keys and tuples of length 2
        as values containing the audit scores and numeric values, respectively.
    """
    audit_results = {}
    # Create results dict with scores and numerical values for each audit.
    for k in audits_base.keys():
        score = audits_base[k].get("score")
        if score is not None:
            num_value = audits_base[k].get("numericValue", "n/a")
            audit_results[k] = (score * 100, num_value)
        else:
            audit_results[k] = ("n/a", "n/a")
    # Sort dict alphabetically so each audit is written to Excel in the same order.
    return sort_dict_alpha(audit_results)


def _parse_metrics(
    audits_base: dict, metrics: list[str]
) -> dict[str, Union[int, float]]:
    """Parses performance metrics from the JSON response to write to Excel.

    Metrics have no scores associated with them.

    Returns:
        A dict of metrics results with metric names as keys
        and int or float metrics as values.
    """
    if "all" in metrics:
        metrics_to_use = copy.copy(COMMAND_CHOICES["metrics"])
        # Remove 'all' to avoid key errors, as it doesn't exist in JSON resp.
        if type(metrics_to_use) == list:
            metrics_to_use.remove("all")
    else:
        metrics_to_use = metrics

    # Create new dict of metrics based on user's chosen metrics.
    metrics_results = {}
    metrics_loc = audits_base["metrics"]["details"]["items"][0]
    metrics_results = {field: metrics_loc[field] for field in metrics_to_use}
    # Sort dict alphabetically so each metric is written to Excel in the same order.
    return sort_dict_alpha(metrics_results)


def _get_audits_base(json_resp: dict) -> dict:
    """Gets the location of audits in the JSON response."""
    return json_resp["lighthouseResult"]["audits"]


def _get_timestamp(json_resp: dict) -> str:
    """Parses the timestamp of the analysis from the JSON response.

    Converts the timestamp to a Python datetime object.

    Returns:
        A str in format year-month-day_hour.minute.second.
    """
    timestamp = json_resp["analysisUTCTimestamp"]
    dt_object = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%fZ")
    date = dt_object.strftime("%Y-%m-%d_%H.%M.%S")
    return date
