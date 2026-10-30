import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def model_cfg(name):
    cfg = json.loads((ROOT / "configs" / "models.json").read_text())[name]
    cfg["name"] = name
    return cfg


def raw_dir(name):
    d = ROOT / "results" / "raw" / name
    d.mkdir(parents=True, exist_ok=True)
    return d
