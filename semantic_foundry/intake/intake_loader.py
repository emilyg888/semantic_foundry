from __future__ import annotations

from pathlib import Path

from semantic_foundry.config import UseCase
from semantic_foundry.intake.use_case_schema import validate_use_case
from semantic_foundry.simple_yaml import load_simple_yaml


def load_use_case(path: Path) -> UseCase:
    payload = load_simple_yaml(path)
    if "use_case" in payload:
        nested = payload["use_case"]
        if not isinstance(nested, dict):
            raise ValueError("use_case must contain a mapping")
        payload = nested
    return validate_use_case(payload)
