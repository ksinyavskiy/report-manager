from grafana_agent.tools.fetch_metrics import fetch_metrics
from grafana_agent.tools.list_available_metrics import list_available_metrics
from grafana_agent.tools.normalize_metrics import normalize_metrics
from grafana_agent.tools.validate_metric_payload import validate_metric_payload


def test_list_available_metrics_known_service():
    result = list_available_metrics("checkout-service")

    assert result["status"] == "success"
    assert result["service"] == "checkout-service"
    assert [metric["name"] for metric in result["metrics"]] == [
        "cpu_usage",
        "memory_usage",
        "error_rate",
        "http_5xx_count",
        "request_latency_p95",
        "request_latency_p99",
    ]
    assert result["error"] is None


def test_list_available_metrics_unknown_service():
    result = list_available_metrics("payment-service")

    assert result["status"] == "failed"
    assert result["metrics"] == []
    assert result["error"]["code"] == "SERVICE_NOT_FOUND"


def test_fetch_metrics_filters_by_time_range():
    result = fetch_metrics(
        service="checkout-service",
        metrics=["error_rate"],
        start="2026-04-25T11:40:00Z",
        end="2026-04-25T12:00:00Z",
    )

    assert result["status"] == "success"
    assert result["raw_metrics"] == [
        {
            "name": "error_rate",
            "unit": "percent",
            "points": [
                {
                    "timestamp": "2026-04-25T11:50:00Z",
                    "value": 4.5,
                }
            ],
        }
    ]


def test_fetch_metrics_missing_metric_returns_warning():
    result = fetch_metrics(
        service="checkout-service",
        metrics=["does_not_exist"],
        start="2026-04-25T11:00:00Z",
        end="2026-04-25T12:00:00Z",
    )

    assert result["status"] == "partial"
    assert result["raw_metrics"] == []
    assert result["warnings"][0]["code"] == "METRIC_NOT_FOUND"


def test_normalize_metrics_converts_values_to_float():
    result = normalize_metrics([
        {
            "name": "http_5xx_count",
            "unit": "count",
            "points": [
                {
                    "timestamp": "2026-04-25T11:30:00Z",
                    "value": 2,
                }
            ],
        }
    ])

    assert result["metrics"][0]["points"][0]["value"] == 2.0


def test_validate_metric_payload_accepts_valid_points():
    result = validate_metric_payload({
        "metrics": [
            {
                "name": "request_latency_p95",
                "unit": "milliseconds",
                "points": [
                    {
                        "timestamp": "2026-04-25T11:00:00Z",
                        "value": 120.0,
                    }
                ],
            }
        ]
    })

    assert result == {
        "valid": True,
        "errors": [],
    }


def test_validate_metric_payload_rejects_invalid_points():
    result = validate_metric_payload({
        "metrics": [
            {
                "name": "request_latency_p95",
                "unit": "milliseconds",
                "points": [
                    {
                        "timestamp": 123,
                        "value": "bad",
                    }
                ],
            }
        ]
    })

    assert result["valid"] is False
    assert [error["code"] for error in result["errors"]] == [
        "INVALID_TIMESTAMP",
        "INVALID_VALUE",
    ]
