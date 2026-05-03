from __future__ import annotations

from semantic_foundry.config import UseCase


def build_ai_context_cards(use_case: UseCase) -> dict[str, object]:
    return {
        "use_case_id": use_case.use_case_id,
        "ai_context_cards": [
            {
                "asset_id": "certified_fraud_alert",
                "business_description": "Contains transactions flagged as suspicious based on candidate fraud signal rules. Fraud alerts are indicators for analyst review, not final determinations of fraud.",
                "approved_questions": use_case.business_questions,
                "allowed_questions": use_case.business_questions,
                "refusal_rule": "Do not state that fraud is confirmed; treat outputs as suspicious activity indicators that require human review.",
                "refusal_rules": [
                    "Refuse to make final fraud determinations about a customer.",
                    "Refuse to recommend adverse action without human investigation.",
                    "Refuse to expose restricted transaction-level details to unauthorised users.",
                ],
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
                "disallowed_questions": [
                    "Is this customer definitely committing fraud?",
                    "Should this customer account be closed automatically?",
                    "Should this transaction be blocked without review?",
                ],
                "required_caveats": [
                    "Fraud alerts are indicators, not final determinations.",
                    "Human review is required.",
                    "Signal thresholds require business approval.",
                    "Evaluation metrics depend on the quality of the available fraud label.",
                ],
                "safe_join_paths": [
                    "certified_fraud_alert.account_id -> certified_business_account.account_id",
                    "certified_business_account.customer_id -> certified_business_customer.customer_id",
                ],
                "default_filters": ["predicted_fraud = true"],
                "sensitive_fields": ["customer_name", "account_id", "txn_id", "transaction_amount"],
            }
        ],
    }
