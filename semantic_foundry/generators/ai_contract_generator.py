from __future__ import annotations

from semantic_foundry.config import UseCase


def build_ai_context_cards(use_case: UseCase) -> dict[str, object]:
    return {
        "use_case_id": use_case.use_case_id,
        "ai_context_cards": [
            {
                "asset_id": "certified_transaction_fraud_signal",
                "approved_questions": use_case.business_questions,
                "refusal_rule": "Do not state that fraud is confirmed; treat outputs as suspicious activity indicators that require human review.",
                "allowed_actions": [
                    "Explain contributing fraud signals",
                    "Summarise recent account behaviour",
                    "Compare transaction to account baseline",
                ],
                "disallowed_actions": [
                    "Auto-close a fraud case",
                    "Notify the customer without analyst approval",
                    "Use uncertified synthetic labels as production truth",
                ],
            }
        ],
    }
