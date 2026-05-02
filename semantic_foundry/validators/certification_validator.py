from __future__ import annotations


def build_issue_register() -> dict[str, object]:
    return {
        "issues": [
            {
                "severity": "high",
                "asset": "fraud_precision",
                "issue": "Synthetic fraud labels are suitable for accelerator validation only.",
                "blocking": True,
            },
            {
                "severity": "medium",
                "asset": "account_had_burst",
                "issue": "Experimental signal requires calibration on production history.",
                "blocking": False,
            },
        ]
    }
