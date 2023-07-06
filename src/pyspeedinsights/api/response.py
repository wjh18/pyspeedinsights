"""Response processing and parsing for PSI API results."""

import json
import logging
from datetime import datetime
from typing import Union

from ..utils.generic import sort_dict_alpha

logger = logging.getLogger(__name__)

METRICS_ABBR = {
    "CUMULATIVE_LAYOUT_SHIFT_SCORE": "CLS",
    "EXPERIMENTAL_INTERACTION_TO_NEXT_PAINT": "INP(E)",
    "EXPERIMENTAL_TIME_TO_FIRST_BYTE": "TTFB(E)",
    "FIRST_CONTENTFUL_PAINT_MS": "FCP",
    "FIRST_INPUT_DELAY_MS": "FID",
    "INTERACTION_TO_NEXT_PAINT": "INP",
    "LARGEST_CONTENTFUL_PAINT_MS": "LCP",
}


def process_json(json_resp: dict, category: str, strategy: str) -> None:
    """Dumps raw json response to a file in the working directory.

    Called within main() in pyspeedinsights.app.
    If json format is selected this is where program execution ends.
    """
    date = _get_timestamp(json_resp)
    filename = f"psi-s-{strategy}-c-{category}-{date}.json"

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(json_resp, f, ensure_ascii=False, indent=4)
        logger.info("JSON processed. Check your current working directory.")


def process_excel(json_resp: dict, category: str) -> dict[str, Union[dict, None]]:
    """Calls various parsing operations for Excel / Sitemap formats.

    Called within main() in pyspeedinsights.app.
    Metrics results are only included if the category is performance.
    """
    json_err = "Malformed JSON response. Skipping Excel processing for URL: "
    try:
        audits_base = _get_audits_base(json_resp)  # Location of audits in json response
        metadata = _parse_metadata(json_resp, category)
        audit_results = _parse_audits(audits_base)
    except KeyError as err:
        logger.error(f"{json_err}{err}", exc_info=True)
        return {}

    if category == "performance":
        try:
            metrics_base = _get_metrics_base(
                json_resp
            )  # Loc of metrics in json response
            metrics_results = _parse_metrics(metrics_base)
        except KeyError as err:
            logger.error(f"Metrics not available for this report: {err}", exc_info=True)
            metrics_results = None
    else:
        logger.warning("Skipping metrics (non-performance category)")
        metrics_results = None

    results: dict[str, Union[dict, None]] = {
        "metadata": metadata,
        "audit_results": audit_results,
        "metrics_results": metrics_results,
    }
    logger.info("Response data processed for URL.")
    return results


def _parse_metadata(json_resp: dict, category: str) -> dict[str, Union[str, int]]:
    """Parses various metadata from the JSON response to write to Excel."""
    logger.info("Parsing metadata from JSON response.")

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
    logger.info("Parsing audit data from JSON response.")

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


def _parse_metrics(metrics_base: dict) -> dict[str, Union[int, float]]:
    """Parses performance metric scores from the JSON response to write to Excel.

    Real-user experience data from CrUX dataset.

    Returns:
        A dict of metrics results with metric names as keys
        and their scores as values.
    """
    logger.info("Parsing metrics data from JSON response.")
    metrics_results = {}
    for metric, result in metrics_base.items():
        try:
            abbr = METRICS_ABBR[metric]
        except KeyError:
            abbr = metric
        score = result["distributions"][0]["proportion"]
        score = round(score, 3) * 100
        metrics_results[abbr] = score
    # Ensure each metric is written to Excel under the same column.
    desired_order_list = ("CLS", "FCP", "LCP", "FID", "INP", "INP(E)", "TTFB(E)")
    return {k: metrics_results[k] for k in desired_order_list}


def _get_audits_base(json_resp: dict) -> dict:
    """Gets the location of audits in the JSON response."""
    return json_resp["lighthouseResult"]["audits"]


def _get_metrics_base(json_resp: dict) -> dict:
    """Gets the location of metrics in the JSON response."""
    return json_resp["loadingExperience"]["metrics"]


def _get_timestamp(json_resp: dict) -> str:
    """Parses the timestamp of the analysis from the JSON response.

    Converts the timestamp to a Python datetime object.

    Returns:
        A str in format year-month-day_hour.minute.second.
    """
    logger.info("Parsing timestamp from JSON response.")
    time_format = "%Y-%m-%d_%H.%M.%S"

    try:
        timestamp = json_resp["analysisUTCTimestamp"]
    except KeyError:
        logger.warning("Unable to parse timestamp. Falling back to local time.")
        date = datetime.now().strftime(time_format)
        return date

    ts_no_fractions = timestamp.split(".")[0]  # Remove fraction
    if ts_no_fractions[-1] != "Z":
        ts_no_fractions += "Z"  # Add Z back after fraction removal
    dt_object = datetime.strptime(ts_no_fractions, "%Y-%m-%dT%H:%M:%SZ")
    date = dt_object.strftime(time_format)
    return date
