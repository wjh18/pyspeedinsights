import pytest

from pyspeedinsights.api.response import (
    _get_audits_base,
    _get_metrics_base,
    _get_timestamp,
    _parse_audits,
    _parse_metadata,
    _parse_metrics,
    process_excel,
)


class TestProcessExcel:
    def _get_json_resp(self, metrics_json, category="performance"):
        return {
            "analysisUTCTimestamp": "2023-02-26T17:36:18",
            "lighthouseResult": {
                "configSettings": {"formFactor": "desktop"},
                "categories": {category: {"score": 1}},
                "audits": {
                    "audit": {"score": 1, "numericValue": 300},
                },
            },
            "loadingExperience": {"metrics": metrics_json},
        }

    def test_process_excel_performance_gets_metrics(self, metrics_json):
        json_resp = self._get_json_resp(metrics_json)
        results = process_excel(json_resp, "performance")
        assert results == {
            "metadata": {
                "category": "performance",
                "category_score": 1,
                "strategy": "desktop",
                "timestamp": "2023-02-26_17.36.18",
            },
            "audit_results": {"audit": (100, 300)},
            "metrics_results": {
                "CLS": 99.0,
                "FCP": 98.0,
                "LCP": 97.0,
                "FID": 96.0,
                "INP": 95.0,
                "INP(E)": 94.0,
                "TTFB(E)": 93.0,
            },
        }

    def test_process_excel_non_performance_excludes_metrics(self, metrics_json):
        json_resp = self._get_json_resp(metrics_json, "seo")
        results = process_excel(json_resp, "seo")
        assert results == {
            "metadata": {
                "category": "seo",
                "category_score": 1,
                "strategy": "desktop",
                "timestamp": "2023-02-26_17.36.18",
            },
            "audit_results": {"audit": (100, 300)},
            "metrics_results": None,
        }


def test_parse_metadata():
    json_resp = {
        "analysisUTCTimestamp": "2023-02-26T17:36:18Z",
        "lighthouseResult": {
            "configSettings": {"formFactor": "desktop"},
            "categories": {"performance": {"score": 1}},
        },
    }
    category = "performance"
    metadata = _parse_metadata(json_resp, category)
    assert metadata == {
        "category": category,
        "category_score": 1,
        "strategy": "desktop",
        "timestamp": "2023-02-26_17.36.18",
    }


class TestParseAudits:
    def test_parse_audits_returns_score_and_value(self):
        audits_base = {"audit": {"score": 1, "numericValue": 300}}
        audit_results = _parse_audits(audits_base)
        assert audit_results == {"audit": (100, 300)}

    def test_parse_audits_no_score_returns_na(self):
        audits_base = {"audit": {"numericValue": 300}}
        audit_results = _parse_audits(audits_base)
        assert audit_results == {"audit": ("n/a", "n/a")}

    def test_parse_audits_no_numeric_value_returns_na_value(self):
        audits_base = {
            "audit": {
                "score": 1,
            }
        }
        audit_results = _parse_audits(audits_base)
        assert audit_results == {"audit": (100, "n/a")}

    def test_parse_audits_no_score_or_numeric_value_returns_na(self):
        audits_base = {"audit": {}}
        audit_results = _parse_audits(audits_base)
        assert audit_results == {"audit": ("n/a", "n/a")}

    def test_parse_audits_orders_alphabetically(self):
        audits_base = {
            "gotit": {"score": 1, "numericValue": 300},
            "audit": {"score": 1, "numericValue": 300},
        }
        audit_results = _parse_audits(audits_base)
        assert audit_results == {"audit": (100, 300), "gotit": (100, 300)}


class TestParseMetrics:
    def test_parse_metrics_scores(self, metrics_json):
        metrics = _parse_metrics(metrics_json)
        assert metrics == {
            "CLS": 99.0,
            "FCP": 98.0,
            "LCP": 97.0,
            "FID": 96.0,
            "INP": 95.0,
            "INP(E)": 94.0,
            "TTFB(E)": 93.0,
        }

    def test_missing_metric_raises_keyerror(self, metrics_json):
        del metrics_json["CUMULATIVE_LAYOUT_SHIFT_SCORE"]
        with pytest.raises(KeyError):
            _parse_metrics(metrics_json)


def test_get_audits_base():
    json_resp = {"lighthouseResult": {"audits": "base"}}
    audits_base = _get_audits_base(json_resp)
    assert audits_base == "base"


def test_get_metrics_base():
    json_resp = {"loadingExperience": {"metrics": "base"}}
    audits_base = _get_metrics_base(json_resp)
    assert audits_base == "base"


def test_get_timestamp():
    json_resp = {"analysisUTCTimestamp": "2023-02-26T17:36:18Z"}
    timestamp = _get_timestamp(json_resp)
    assert timestamp == "2023-02-26_17.36.18"


def test_get_timestamp_fraction_removed():
    json_resp = {"analysisUTCTimestamp": "2023-02-26T17:36:18.123Z"}
    timestamp = _get_timestamp(json_resp)
    assert timestamp == "2023-02-26_17.36.18"
