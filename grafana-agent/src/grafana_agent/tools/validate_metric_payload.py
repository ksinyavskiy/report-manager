def validate_metric_payload(payload: dict) -> dict:
    errors = []

    for index, metric in enumerate(payload.get("metrics", [])):
        for point_index, point in enumerate(metric.get("points", [])):
            if not isinstance(point.get("timestamp"), str):
                errors.append({
                    "code": "INVALID_TIMESTAMP",
                    "message": "Metric point timestamp must be a string",
                    "details": {
                        "metric_index": index,
                        "point_index": point_index
                    }
                })

            if not isinstance(point.get("value"), (int, float)):
                errors.append({
                    "code": "INVALID_VALUE",
                    "message": "Metric point value must be numeric",
                    "details": {
                        "metric_index": index,
                        "point_index": point_index
                    }
                })

    return {
        "valid": not errors,
        "errors": errors
    }
