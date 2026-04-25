import re
from datetime import datetime, timedelta, timezone

from grafana_agent.tools.fetch_metrics import fetch_metrics
from grafana_agent.tools.list_available_metrics import list_available_metrics
from grafana_agent.tools.normalize_metrics import normalize_metrics
from grafana_agent.tools.validate_metric_payload import validate_metric_payload


METRICS_BY_INTENT = {
    "latency": ["request_latency_p95", "request_latency_p99"],
    "errors": ["error_rate", "http_5xx_count"],
    "resource_usage": ["cpu_usage", "memory_usage"],
    "general_health": ["cpu_usage", "memory_usage", "error_rate", "request_latency_p95"]
}


def run_grafana_agent(input_payload: dict) -> dict:
    output, _tool_trace = run_grafana_agent_with_trace(input_payload)
    return output


def run_grafana_agent_with_trace(input_payload: dict) -> tuple[dict, list[dict]]:
    request_id = input_payload["request_id"]
    task = input_payload["task"]
    context = input_payload["context"]

    service = resolve_service(task, context.get("default_service"))
    metric_intent = resolve_metric_intent(task)
    time_range_result = resolve_time_range(task, context)

    if time_range_result["error"] is not None:
        return failed_output(
            request_id=request_id,
            service=service,
            code="INVALID_TIME_RANGE",
            message=time_range_result["error"],
            details={},
            time_range=None,
            metric_intent=None,
        ), []

    if service is None:
        return failed_output(
            request_id=request_id,
            service=None,
            code="SERVICE_NOT_SPECIFIED",
            message="No service was specified and no default service is available",
            details={},
            time_range=time_range_result["time_range"],
            metric_intent=metric_intent,
        ), []

    tool_trace = []

    tool_trace.append({
        "tool": "list_available_metrics",
        "args": {
            "service": service
        }
    })
    available_metrics_result = list_available_metrics(service)

    if available_metrics_result["status"] == "failed":
        return failed_output(
            request_id=request_id,
            service=service,
            code=available_metrics_result["error"]["code"],
            message=available_metrics_result["error"]["message"],
            details=available_metrics_result["error"]["details"],
            time_range=time_range_result["time_range"],
            metric_intent=metric_intent,
        ), tool_trace

    selected_metrics = select_metrics(metric_intent, available_metrics_result["metrics"])
    start = time_range_result["time_range"]["from"]
    end = time_range_result["time_range"]["to"]

    tool_trace.append({
        "tool": "fetch_metrics",
        "args": {
            "service": service,
            "metrics": selected_metrics,
            "from": start,
            "to": end
        }
    })
    raw_metrics_result = fetch_metrics(service, selected_metrics, start, end)

    if raw_metrics_result["status"] == "failed":
        return failed_output(
            request_id=request_id,
            service=service,
            code=raw_metrics_result["error"]["code"],
            message=raw_metrics_result["error"]["message"],
            details=raw_metrics_result["error"]["details"],
            time_range=time_range_result["time_range"],
            metric_intent=metric_intent,
        ), tool_trace

    tool_trace.append({
        "tool": "normalize_metrics",
        "args": {
            "service": service
        }
    })
    normalized_metrics_result = normalize_metrics(raw_metrics_result["raw_metrics"])

    output = {
        "request_id": request_id,
        "agent": "grafana-agent",
        "status": "success",
        "service": service,
        "time_range": time_range_result["time_range"],
        "metric_intent": metric_intent,
        "selected_metrics": selected_metrics,
        "metrics": normalized_metrics_result["metrics"],
        "warnings": raw_metrics_result["warnings"],
        "error": None,
        "handoff": {
            "next_agent": "metric-analyzer-agent",
            "reason": "metrics_ready_for_analysis"
        }
    }

    tool_trace.append({
        "tool": "validate_metric_payload",
        "args": {
            "service": service
        }
    })
    validation_result = validate_metric_payload(output)

    if not validation_result["valid"]:
        return failed_output(
            request_id=request_id,
            service=service,
            code="PAYLOAD_VALIDATION_FAILED",
            message="Metric payload validation failed",
            details={
                "errors": validation_result["errors"]
            },
            time_range=time_range_result["time_range"],
            metric_intent=metric_intent,
        ), tool_trace

    return output, tool_trace


def resolve_service(task: str, default_service: str | None) -> str | None:
    match = re.search(r"\b[a-z0-9-]+-service\b", task.lower())
    if match:
        return match.group(0)
    return default_service


def resolve_metric_intent(task: str) -> str:
    normalized_task = task.lower()

    if any(keyword in normalized_task for keyword in ("latency", "slow", "p95", "p99")):
        return "latency"

    if any(keyword in normalized_task for keyword in ("error", "errors", "5xx", "fail")):
        return "errors"

    if any(keyword in normalized_task for keyword in ("cpu", "memory", "resource")):
        return "resource_usage"

    return "general_health"


def select_metrics(metric_intent: str, available_metrics: list[dict]) -> list[str]:
    available_names = {metric["name"] for metric in available_metrics}
    return [
        metric_name
        for metric_name in METRICS_BY_INTENT[metric_intent]
        if metric_name in available_names
    ]


def resolve_time_range(task: str, context: dict) -> dict:
    now = parse_iso_datetime(context["now"])
    normalized_task = task.lower()
    explicit_range = re.search(r"from\s+(\d{1,2}:\d{2})\s+to\s+(\d{1,2}:\d{2})", normalized_task)

    if explicit_range:
        start_at = time_on_same_day(now, explicit_range.group(1))
        end_at = time_on_same_day(now, explicit_range.group(2))

        if start_at >= end_at:
            return {
                "time_range": None,
                "error": "Start time must be before end time"
            }

        return {
            "time_range": {
                "from": format_iso_datetime(start_at),
                "to": format_iso_datetime(end_at)
            },
            "error": None
        }

    minutes_match = re.search(r"last\s+(\d+)\s+minutes?", normalized_task)

    if minutes_match:
        minutes = int(minutes_match.group(1))
    elif "last hour" in normalized_task:
        minutes = 60
    else:
        minutes = int(context.get("default_time_range_minutes", 60))

    start_at = now - timedelta(minutes=minutes)
    return {
        "time_range": {
            "from": format_iso_datetime(start_at),
            "to": format_iso_datetime(now)
        },
        "error": None
    }


def failed_output(
    request_id: str,
    service: str | None,
    code: str,
    message: str,
    details: dict,
    time_range: dict | None,
    metric_intent: str | None,
) -> dict:
    return {
        "request_id": request_id,
        "agent": "grafana-agent",
        "status": "failed",
        "service": service,
        "time_range": time_range,
        "metric_intent": metric_intent,
        "selected_metrics": [],
        "metrics": [],
        "warnings": [],
        "error": {
            "code": code,
            "message": message,
            "details": details
        },
        "handoff": None
    }


def parse_iso_datetime(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def time_on_same_day(reference: datetime, hhmm: str) -> datetime:
    hour, minute = [int(part) for part in hhmm.split(":")]
    return datetime(
        year=reference.year,
        month=reference.month,
        day=reference.day,
        hour=hour,
        minute=minute,
        tzinfo=timezone.utc
    )


def format_iso_datetime(value: datetime) -> str:
    return value.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
