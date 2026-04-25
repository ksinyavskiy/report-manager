def normalize_metrics(raw_metrics: list[dict]) -> dict:
    normalized_metrics = []

    for metric in raw_metrics:
        normalized_metrics.append({
            "name": metric["name"],
            "unit": metric["unit"],
            "points": [
                {
                    "timestamp": point["timestamp"],
                    "value": float(point["value"])
                }
                for point in metric["points"]
            ]
        })

    return {
        "status": "success",
        "metrics": normalized_metrics,
        "warnings": [],
        "error": None
    }
