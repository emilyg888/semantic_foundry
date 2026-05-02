from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def dump_yaml(data: Any, indent: int = 0) -> str:
    if isinstance(data, dict):
        lines: list[str] = []
        for key, value in data.items():
            if isinstance(value, (dict, list)):
                lines.append(f'{" " * indent}{key}:')
                lines.append(dump_yaml(value, indent + 2))
            else:
                lines.append(f'{" " * indent}{key}: {format_scalar(value)}')
        return "\n".join(lines)

    if isinstance(data, list):
        lines = []
        for item in data:
            prefix = " " * indent + "-"
            if isinstance(item, (dict, list)):
                lines.append(prefix)
                lines.append(dump_yaml(item, indent + 2))
            else:
                lines.append(f"{prefix} {format_scalar(item)}")
        return "\n".join(lines)

    return " " * indent + format_scalar(data)


def format_scalar(value: Any) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    return json.dumps(str(value))


def load_simple_yaml(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")

    try:
        parsed = json.loads(text)
    except json.JSONDecodeError:
        parsed = parse_indented_yaml(text)

    if not isinstance(parsed, dict):
        raise ValueError(f"{path} must contain a top-level mapping")
    return parsed


def parse_indented_yaml(text: str) -> Any:
    lines = [line.rstrip() for line in text.splitlines() if line.strip() and not line.lstrip().startswith("#")]
    value, next_index = parse_block(lines, 0, 0)
    if next_index != len(lines):
        raise ValueError("Unexpected trailing content in YAML file")
    return value


def parse_block(lines: list[str], start: int, indent: int) -> tuple[Any, int]:
    if start >= len(lines):
        return {}, start

    current_indent = line_indent(lines[start])
    if current_indent != indent:
        raise ValueError(f"Invalid indentation at line: {lines[start]}")

    if lines[start].lstrip().startswith("- "):
        return parse_list(lines, start, indent)
    return parse_mapping(lines, start, indent)


def parse_mapping(lines: list[str], start: int, indent: int) -> tuple[dict[str, Any], int]:
    result: dict[str, Any] = {}
    index = start
    while index < len(lines):
        raw = lines[index]
        current_indent = line_indent(raw)
        if current_indent < indent:
            break
        if current_indent > indent:
            raise ValueError(f"Unexpected indentation at line: {raw}")
        stripped = raw.strip()
        if stripped.startswith("- "):
            break
        key, _, remainder = stripped.partition(":")
        if not _:
            raise ValueError(f"Invalid mapping line: {raw}")
        key = key.strip()
        remainder = remainder.strip()
        index += 1
        if remainder:
            result[key] = parse_scalar(remainder)
            continue
        if index >= len(lines) or line_indent(lines[index]) <= indent:
            result[key] = {}
            continue
        nested, index = parse_block(lines, index, indent + 2)
        result[key] = nested
    return result, index


def parse_list(lines: list[str], start: int, indent: int) -> tuple[list[Any], int]:
    result: list[Any] = []
    index = start
    while index < len(lines):
        raw = lines[index]
        current_indent = line_indent(raw)
        if current_indent < indent:
            break
        if current_indent != indent:
            raise ValueError(f"Unexpected indentation at line: {raw}")
        stripped = raw.strip()
        if not stripped.startswith("- "):
            break
        remainder = stripped[2:].strip()
        index += 1
        if remainder:
            result.append(parse_scalar(remainder))
            continue
        nested, index = parse_block(lines, index, indent + 2)
        result.append(nested)
    return result, index


def parse_scalar(token: str) -> Any:
    if token in {"true", "false"}:
        return token == "true"
    if token == "null":
        return None
    if token.startswith('"') and token.endswith('"'):
        return json.loads(token)
    if token.startswith("'") and token.endswith("'"):
        return token[1:-1]
    try:
        return int(token)
    except ValueError:
        pass
    try:
        return float(token)
    except ValueError:
        pass
    return token


def line_indent(line: str) -> int:
    return len(line) - len(line.lstrip(" "))
