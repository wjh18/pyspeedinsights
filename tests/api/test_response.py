from pyspeedinsights.api.response import (
    _get_audits_base,
    _get_timestamp,
    _parse_audits,
    _parse_metadata,
    _parse_metrics,
)


def test_parse_metadata():
    json_resp = {
        "analysisUTCTimestamp": "2023-02-26T17:36:18.266Z",
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
    def test_parse_metrics_all(self, all_metrics):
        audits_base = {"metrics": {"details": {"items": [all_metrics]}}}
        metrics_to_use = ["all"]
        metrics = _parse_metrics(audits_base, metrics_to_use)
        assert metrics == all_metrics

    def test_parse_metrics_custom(self, all_metrics):
        audits_base = {"metrics": {"details": {"items": [all_metrics]}}}
        metrics_to_use = ["observedFirstPaint", "totalCumulativeLayoutShift"]
        metrics = _parse_metrics(audits_base, metrics_to_use)
        assert metrics == {
            "observedFirstPaint": 115,
            "totalCumulativeLayoutShift": 0,
        }


def test_get_audits_base():
    json_resp = {"lighthouseResult": {"audits": "base"}}
    audits_base = _get_audits_base(json_resp)
    assert audits_base == "base"


def test_get_timestamp():
    json_resp = {"analysisUTCTimestamp": "2023-02-26T17:36:18.266Z"}
    timestamp = _get_timestamp(json_resp)
    assert timestamp == "2023-02-26_17.36.18"
