from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class ReviewAsset:
    asset_type: str
    asset_id: str
    display_name: str
    owner: str
    status: str
    file_key: str
    index: int
    source_references: list[str]


@dataclass(slots=True)
class ApprovalRecord:
    asset_type: str
    asset_id: str
    decision: str
    reviewer: str
    comments: str
    updated_at: str

    def as_dict(self) -> dict[str, object]:
        return {
            "asset_type": self.asset_type,
            "asset_id": self.asset_id,
            "decision": self.decision,
            "reviewer": self.reviewer,
            "comments": self.comments,
            "updated_at": self.updated_at,
        }
