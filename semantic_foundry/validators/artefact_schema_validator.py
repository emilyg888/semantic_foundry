from __future__ import annotations


REQUIRED_KEYS = {
    "glossary": ("use_case_id", "generated_terms"),
    "entities": ("use_case_id", "entities"),
    "relationships": ("use_case_id", "relationships"),
    "metrics": ("use_case_id", "metrics"),
    "signals": ("use_case_id", "signals"),
    "predictions": ("use_case_id", "predictions"),
    "dq_rules": ("use_case_id", "dq_rules"),
    "policies": ("use_case_id", "policies"),
    "ai_context_cards": ("use_case_id", "ai_context_cards"),
    "semantic_manifest": ("run",),
}


def validate_artefacts(artefacts: dict[str, object]) -> None:
    for artefact_name, required_keys in REQUIRED_KEYS.items():
        if artefact_name not in artefacts:
            raise ValueError(f"Missing artefact: {artefact_name}")
        payload = artefacts[artefact_name]
        if not isinstance(payload, dict):
            raise ValueError(f"Artefact {artefact_name} must be a mapping")
        missing = [key for key in required_keys if key not in payload]
        if missing:
            raise ValueError(f"Artefact {artefact_name} is missing keys: {', '.join(missing)}")

    if len(artefacts["glossary"]["generated_terms"]) < 5:  # type: ignore[index]
        raise ValueError("Glossary must contain at least 5 generated terms")
    if len(artefacts["entities"]["entities"]) < 3:  # type: ignore[index]
        raise ValueError("Entity model must contain at least 3 entities")
    if len(artefacts["signals"]["signals"]) < 3:  # type: ignore[index]
        raise ValueError("Signal catalogue must contain at least 3 signals")
    if len(artefacts["dq_rules"]["dq_rules"]) < 3:  # type: ignore[index]
        raise ValueError("DQ rules must contain at least 3 checks")
