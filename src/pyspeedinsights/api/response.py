import copy
import json
from datetime import datetime

from ..cli.choices import COMMAND_CHOICES


def process_json(json_resp, category, strategy):
    """Dump raw json response to a file in the working directory."""

    date = _get_timestamp(json_resp)
    filename = f"psi-s-{strategy}-c-{category}-{date}.json"

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(json_resp, f, ensure_ascii=False, indent=4)
        print("JSON processed. Check your current directory.")


def process_excel(json_resp, category, metrics):
    """Call various parsing operations for Excel / Sitemap formats."""

    audits_base = _get_audits_base(json_resp)  # Location of audits in json response

    metadata = _parse_metadata(json_resp, category)
    audit_results = _parse_audits(audits_base)

    # Metrics are only available in the performance category.
    if metrics is not None and category == "performance":
        metrics_results = _parse_metrics(audits_base, metrics)
    else:
        metrics_results = None

    results = {
        "metadata": metadata,
        "audit_results": audit_results,
        "metrics_results": metrics_results,
    }

    return results


def _parse_metadata(json_resp, category):
    """Parse various metadata from the JSON response to write to Excel."""

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


def _parse_audits(audits_base):
    """Parse Lighthouse audits from the JSON response to write to Excel."""

    audit_results = {}

    # Create results dict with scores and numerical values for each audit.
    for k in audits_base.keys():
        score = audits_base[k].get("score")
        if score is not None:
            num_value = audits_base[k].get("numericValue", "n/a")
            audit_results[k] = [score * 100, num_value]
        else:
            audit_results[k] = ["n/a", "n/a"]

    # Sort dict alphabetically so each audit is written to Excel in the same order.
    audit_results = dict(sorted(audit_results.items()))

    return audit_results


def _parse_metrics(audits_base, metrics):
    """Parse performance metrics from the JSON response to write to Excel."""

    metrics_results = {}
    metrics_loc = audits_base["metrics"]["details"]["items"][0]

    if "all" in metrics:
        metrics_to_use = copy.copy(COMMAND_CHOICES["metrics"])
        # Remove 'all' to avoid key errors, as it doesn't exist in JSON resp.
        metrics_to_use.remove("all")
    else:
        metrics_to_use = metrics

    # Create new dict of metrics based on user's chosen metrics.
    for field in metrics_to_use:
        metric = metrics_loc[field]
        metrics_results[field] = metric

    # Sort dict alphabetically so each metric is written to Excel in the same order.
    metrics_results = dict(sorted(metrics_results.items()))

    return metrics_results


def _get_audits_base(json_resp):
    """Return the location of audits in the JSON response."""

    return json_resp["lighthouseResult"]["audits"]


def _get_timestamp(json_resp):
    """
    Parse the timestamp of the analysis from the JSON response.

    Covert it to a Python datetime object.
    """

    timestamp = json_resp["analysisUTCTimestamp"]
    date = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%fZ")

    return date
