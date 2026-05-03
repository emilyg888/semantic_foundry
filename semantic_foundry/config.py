from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass(slots=True)
class UseCase:
    use_case_id: str
    business_objective: str
    primary_users: list[str]
    business_questions: list[str]
    decision_type: str
    automation_level: str
    risk_level: str
    in_scope_entities: list[str] = field(default_factory=list)
    in_scope_signals: list[str] = field(default_factory=list)
    owners: dict[str, str] = field(default_factory=dict)
    source_dataset_names: list[str] = field(default_factory=list)
    target: str = "generic_sql"


@dataclass(slots=True)
class BuildRequest:
    source_path: Path
    use_case_path: Path
    output_root: Path
    target: str = "generic_sql"


@dataclass(slots=True)
class SourceFile:
    path: str
    category: str
    suffix: str
    role: str | None = None


@dataclass(slots=True)
class FunctionLogic:
    module_path: str
    function_name: str
    assigned_names: list[str]
    compared_names: list[str]
    called_names: list[str]
    return_names: list[str]


@dataclass(slots=True)
class InventorySummary:
    root: str
    files: list[SourceFile]

    @property
    def counts_by_category(self) -> dict[str, int]:
        counts: dict[str, int] = {}
        for item in self.files:
            counts[item.category] = counts.get(item.category, 0) + 1
        return counts
