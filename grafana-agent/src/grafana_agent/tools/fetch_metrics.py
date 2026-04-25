from datetime import datetime

from grafana_agent.tools._fixtures import load_fake_grafana_json


def parse_timestamp(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def metric_units(service: str) -> dict[str, str]:
    catalog = load_fake_grafana_json("metrics_catalog.json")
    return {
        metric["name"]: metric["unit"]
        for metric in catalog.get(service, [])
    }


def fetch_metrics(service: str, metrics: list[str], start: str, end: str) -> dict:
    series = load_fake_grafana_json("time_series.json")
    units = metric_units(service)

    if service not in series:
        return {
            "status": "failed",
            "source": "fake_grafana",
            "service": service,
            "raw_metrics": [],
            "warnings": [],
            "error": {
                "code": "SERVICE_NOT_FOUND",
                "message": f"No time series found for service {service}",
                "details": {
                    "service": service
                }
            }
        }

    start_at = parse_timestamp(start)
    end_at = parse_timestamp(end)
    raw_metrics = []
    warnings = []

    for metric_name in metrics:
        points = series[service].get(metric_name)

        if points is None:
            warnings.append({
                "code": "METRIC_NOT_FOUND",
                "message": f"Metric {metric_name} was not found for service {service}",
                "details": {
                    "metric": metric_name,
                    "service": service
                }
            })
            continue

        filtered_points = [
            point
            for point in points
            if start_at <= parse_timestamp(point["timestamp"]) <= end_at
        ]
        raw_metrics.append({
            "name": metric_name,
            "unit": units.get(metric_name, "unknown"),
            "points": filtered_points
        })

    return {
        "status": "success" if not warnings else "partial",
        "source": "fake_grafana",
        "service": service,
        "raw_metrics": raw_metrics,
        "warnings": warnings,
        "error": None
    }
