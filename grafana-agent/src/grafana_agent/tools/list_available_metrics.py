from grafana_agent.tools._fixtures import load_fake_grafana_json


def list_available_metrics(service: str) -> dict:
    catalog = load_fake_grafana_json("metrics_catalog.json")

    if service not in catalog:
        return {
            "status": "failed",
            "service": service,
            "metrics": [],
            "warnings": [],
            "error": {
                "code": "SERVICE_NOT_FOUND",
                "message": f"No metrics catalog found for service {service}",
                "details": {
                    "service": service
                }
            }
        }

    return {
        "status": "success",
        "service": service,
        "metrics": catalog[service],
        "warnings": [],
        "error": None
    }
