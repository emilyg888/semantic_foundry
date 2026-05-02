from __future__ import annotations


REFERENCE_GLOSSARY = {
    "customer": {
        "definition": "A business customer that owns or controls one or more SME banking accounts.",
        "owner": "Head of Business Banking",
        "synonyms": ["business customer", "SME customer"],
        "sensitivity": "confidential",
    },
    "account": {
        "definition": "A banking account used to originate or receive SME business transactions.",
        "owner": "Head of Business Banking",
        "synonyms": ["business account"],
        "sensitivity": "confidential",
    },
    "transaction": {
        "definition": "A single transaction event recorded against an account.",
        "owner": "Fraud Operations Lead",
        "synonyms": ["payment event", "banking transaction"],
        "sensitivity": "restricted",
    },
    "merchant": {
        "definition": "A merchant or counterparty receiving or originating business banking transactions.",
        "owner": "Fraud Operations Lead",
        "synonyms": ["counterparty", "merchant counterparty"],
        "sensitivity": "confidential",
    },
    "fraud_label": {
        "definition": "The available fraud outcome label used for accelerator evaluation and model-quality measurement.",
        "owner": "Fraud Analytics Lead",
        "synonyms": ["fraud flag", "evaluation label"],
        "sensitivity": "internal",
    },
    "model_run": {
        "definition": "A detector evaluation run that aggregates fraud prediction outcomes across a set of transactions.",
        "owner": "Fraud Analytics Lead",
        "synonyms": ["detector run", "evaluation run"],
        "sensitivity": "internal",
    },
    "fraud_signal": {
        "definition": "A derived indicator that suggests suspicious behaviour requiring analyst review.",
        "owner": "Fraud Risk Owner",
        "synonyms": ["risk signal", "alert signal"],
        "sensitivity": "restricted",
    },
    "fraud_alert": {
        "definition": "A transaction or account state that crosses suspicious activity thresholds.",
        "owner": "Fraud Operations Lead",
        "synonyms": ["alert", "case candidate"],
        "sensitivity": "restricted",
    },
    "fraud_score": {
        "definition": "A composite score representing the intensity of suspicious transaction behaviour.",
        "owner": "Fraud Analytics Lead",
        "synonyms": ["risk score"],
        "sensitivity": "internal",
    },
    "burst_activity": {
        "definition": "A short concentration of transactions that may indicate abnormal velocity or coordination.",
        "owner": "Fraud Risk Owner",
        "synonyms": ["temporal burst", "velocity burst"],
        "sensitivity": "restricted",
    },
    "synthetic_fraud_label": {
        "definition": "A generated label used for accelerator testing, not a production-confirmed fraud outcome.",
        "owner": "Fraud Analytics Lead",
        "synonyms": ["training label", "synthetic label"],
        "sensitivity": "internal",
    },
}

REFERENCE_ENTITIES = [
    {
        "entity_id": "certified_business_customer",
        "name": "customer",
        "definition": "Business customer master entity for SME fraud analysis.",
        "grain": "one row per business customer",
        "primary_key": "customer_id",
        "owner": "Head of Business Banking",
        "source_table": "customers",
        "certification_status": "draft",
    },
    {
        "entity_id": "certified_business_account",
        "name": "account",
        "definition": "Business account entity linked to a customer.",
        "grain": "one row per account",
        "primary_key": "account_id",
        "owner": "Head of Business Banking",
        "source_table": "accounts",
        "certification_status": "candidate",
    },
    {
        "entity_id": "certified_transaction",
        "name": "transaction",
        "definition": "Transaction event with fraud-relevant behaviour and labels.",
        "grain": "one row per transaction event",
        "primary_key": "txn_id",
        "owner": "Fraud Operations Lead",
        "source_table": "transactions",
        "certification_status": "candidate",
    },
    {
        "entity_id": "certified_merchant",
        "name": "merchant",
        "definition": "Merchant or counterparty entity used to analyse fraud concentration and merchant risk patterns.",
        "grain": "one row per merchant",
        "primary_key": "merchant_id",
        "owner": "Fraud Operations Lead",
        "source_table": "transactions",
        "certification_status": "draft",
    },
    {
        "entity_id": "certified_fraud_model_run",
        "name": "model_run",
        "definition": "Fraud detector evaluation run entity for aggregated model-quality metrics.",
        "grain": "one row per detector evaluation run",
        "primary_key": "model_run_id",
        "owner": "Fraud Analytics Lead",
        "source_table": "evaluation::fraud_detector",
        "certification_status": "draft",
    },
]

REFERENCE_RELATIONSHIPS = [
    {
        "from_entity": "certified_business_customer",
        "to_entity": "certified_business_account",
        "relationship": "owns",
        "join_keys": ["customer_id"],
        "cardinality": "1_to_many",
    },
    {
        "from_entity": "certified_business_account",
        "to_entity": "certified_transaction",
        "relationship": "has",
        "join_keys": ["account_id"],
        "cardinality": "1_to_many",
    },
    {
        "from_entity": "certified_transaction",
        "to_entity": "certified_merchant",
        "relationship": "occurs_at",
        "join_keys": ["merchant_id"],
        "cardinality": "many_to_one",
    },
    {
        "from_entity": "certified_merchant",
        "to_entity": "certified_transaction",
        "relationship": "accepts",
        "join_keys": ["merchant_id"],
        "cardinality": "1_to_many",
    },
    {
        "from_entity": "certified_business_account",
        "to_entity": "certified_merchant",
        "relationship": "transacts_with",
        "join_keys": ["merchant_id"],
        "cardinality": "many_to_many",
    },
]

REFERENCE_METRICS = [
    {
        "metric_id": "fraud_alert_volume",
        "name": "Fraud Alert Volume",
        "metric_type": "operational_metric",
        "evaluation_subject": "fraud_alert",
        "definition": "Count of suspicious transactions flagged for analyst review.",
        "grain": "day",
        "formula": "count(case when predicted_fraud = 1 then txn_id end)",
        "required_inputs": ["predicted_fraud", "txn_id"],
        "owner": "Fraud Operations Lead",
        "status": "candidate",
        "interpretation": {
            "high_value_means": "More suspicious transactions are being surfaced for analyst review.",
            "low_value_means": "Fewer suspicious transactions are being surfaced for analyst review.",
        },
    },
    {
        "metric_id": "fraud_precision",
        "name": "Fraud Precision",
        "metric_type": "evaluation_metric",
        "evaluation_subject": "fraud_detector",
        "definition": "Proportion of flagged transactions that match the available fraud label.",
        "grain": "model_run",
        "formula": "true_positive / nullif(true_positive + false_positive, 0)",
        "required_inputs": ["true_positive", "false_positive", "predicted_fraud", "fraud_label"],
        "owner": "Fraud Analytics Lead",
        "status": "draft",
        "interpretation": {
            "high_value_means": "Fewer false positive alerts.",
            "low_value_means": "Many flagged transactions do not match the available fraud label.",
        },
    },
    {
        "metric_id": "fraud_recall",
        "name": "Fraud Recall",
        "metric_type": "evaluation_metric",
        "evaluation_subject": "fraud_detector",
        "definition": "Proportion of labelled fraud transactions that were flagged by the detector.",
        "grain": "model_run",
        "formula": "true_positive / nullif(true_positive + false_negative, 0)",
        "required_inputs": ["true_positive", "false_negative", "predicted_fraud", "fraud_label"],
        "owner": "Fraud Analytics Lead",
        "status": "draft",
        "interpretation": {
            "high_value_means": "More labelled fraud transactions are detected.",
            "low_value_means": "More labelled fraud transactions are missed.",
        },
    },
    {
        "metric_id": "false_positive_rate",
        "name": "False Positive Rate",
        "metric_type": "evaluation_metric",
        "evaluation_subject": "fraud_detector",
        "definition": "Proportion of legitimate transactions incorrectly flagged as fraud.",
        "grain": "model_run",
        "formula": "false_positive / nullif(false_positive + true_negative, 0)",
        "required_inputs": ["false_positive", "true_negative", "predicted_fraud", "fraud_label"],
        "owner": "Fraud Analytics Lead",
        "status": "draft",
        "interpretation": {
            "high_value_means": "Too many legitimate transactions are being flagged.",
            "low_value_means": "Fewer legitimate transactions are being incorrectly flagged.",
        },
    },
    {
        "metric_id": "false_negative_rate",
        "name": "False Negative Rate",
        "metric_type": "evaluation_metric",
        "evaluation_subject": "fraud_detector",
        "definition": "Proportion of fraud-labelled transactions missed by the detector.",
        "grain": "model_run",
        "formula": "false_negative / nullif(false_negative + true_positive, 0)",
        "required_inputs": ["false_negative", "true_positive", "predicted_fraud", "fraud_label"],
        "owner": "Fraud Analytics Lead",
        "status": "draft",
        "interpretation": {
            "high_value_means": "Too many fraud-labelled transactions are missed.",
            "low_value_means": "Fewer fraud-labelled transactions are missed.",
        },
    },
    {
        "metric_id": "f1_score",
        "name": "F1 Score",
        "metric_type": "evaluation_metric",
        "evaluation_subject": "fraud_detector",
        "definition": "Balanced evaluation metric combining fraud precision and fraud recall using the harmonic mean for the detector run.",
        "grain": "model_run",
        "formula": "2 * ((precision * recall) / nullif(precision + recall, 0))",
        "required_inputs": ["precision", "recall", "predicted_fraud", "fraud_label"],
        "owner": "Fraud Analytics Lead",
        "status": "draft",
        "interpretation": {
            "high_value_means": "The detector is performing well when the business cares about both alert quality and detection coverage.",
            "low_value_means": "The detector is imbalanced on precision, recall, or both, so overall performance is weaker.",
        },
    },
]

REFERENCE_SIGNALS = {
    "amount_spike_signal": {
        "definition": "Signal indicating unusually large transaction amounts relative to absolute and statistical thresholds.",
        "logic": "abs_amount > 15000 or z_score >= 3",
        "required_inputs": ["amount", "abs_amount", "z_score"],
        "status": "candidate",
    },
    "velocity_burst_signal": {
        "definition": "Signal indicating suspicious transaction velocity or same-timestamp bursts.",
        "logic": "txn_count >= 10 or same_ts_count >= 3 or is_burst = true",
        "required_inputs": ["txn_count", "same_ts_count", "is_burst"],
        "status": "candidate",
    },
    "statistical_anomaly_signal": {
        "definition": "Signal indicating transaction behaviour that deviates from customer or account baseline patterns.",
        "logic": "z_score >= 3 or account_zscore >= 2.5 or is_anomaly = true",
        "required_inputs": ["z_score", "account_zscore", "is_anomaly"],
        "status": "candidate",
    },
    "account_burst_history_signal": {
        "definition": "Signal indicating that the account has a recent history of burst-like behaviour.",
        "logic": "account_had_burst = true",
        "required_inputs": ["account_had_burst", "is_burst"],
        "status": "experimental",
    },
}

REFERENCE_PREDICTIONS = {
    "predicted_fraud": {
        "definition": "Rule-based fraud prediction output.",
        "logic": "is_spike or is_velocity or is_anomaly or is_burst",
        "prediction_type": "alert_prediction",
        "required_inputs": ["is_spike", "is_velocity", "is_anomaly", "is_burst"],
        "status": "candidate",
    },
    "fraud_score": {
        "definition": "Composite weighted fraud score.",
        "logic": "weighted sum of suspicious signals",
        "prediction_type": "risk_score",
        "required_inputs": ["is_spike", "is_velocity", "is_anomaly", "is_burst"],
        "status": "candidate",
    },
}

REFERENCE_DQ_RULES = [
    {
        "rule_id": "dq_transactions_primary_key",
        "asset": "certified_transaction",
        "severity": "critical",
        "check": "txn_id must be unique and non-null",
    },
    {
        "rule_id": "dq_accounts_customer_fk",
        "asset": "certified_business_account",
        "severity": "high",
        "check": "customer_id must resolve to an existing customer",
    },
    {
        "rule_id": "dq_transactions_account_fk",
        "asset": "certified_transaction",
        "severity": "critical",
        "check": "account_id must resolve to an existing account",
    },
    {
        "rule_id": "dq_transactions_timestamp",
        "asset": "certified_transaction",
        "severity": "high",
        "check": "timestamp must be present and parseable",
    },
    {
        "rule_id": "dq_transactions_merchant_fk",
        "asset": "certified_transaction",
        "severity": "high",
        "check": "merchant_id should resolve to a merchant semantic entity when present",
    },
]

REFERENCE_POLICIES = [
    {
        "policy_id": "policy_transaction_restricted",
        "asset": "certified_transaction",
        "classification": "restricted",
        "approved_use": "Fraud triage, analyst review, model monitoring",
        "disallowed_use": "Unrestricted AI summarisation or customer-facing automation",
    },
    {
        "policy_id": "policy_synthetic_label_caveat",
        "asset": "fraud_precision",
        "classification": "internal",
        "approved_use": "Accelerator validation only",
        "disallowed_use": "Production fraud outcome reporting",
    },
]
