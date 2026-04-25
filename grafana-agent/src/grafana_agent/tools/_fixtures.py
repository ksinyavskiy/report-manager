import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[3]
FAKE_GRAFANA_DIR = PROJECT_ROOT / "fixtures" / "fake_grafana"


def load_fake_grafana_json(filename: str):
    with (FAKE_GRAFANA_DIR / filename).open("r", encoding="utf-8") as file:
        return json.load(file)
