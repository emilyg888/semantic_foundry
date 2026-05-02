from __future__ import annotations


def predict_fraud(features: dict[str, float | bool]) -> dict[str, float | bool]:
    is_spike = bool(features["abs_amount"] > 15000 or features["z_score"] >= 3)
    is_velocity = bool(features["txn_count"] >= 10)
    is_anomaly = bool(features["account_zscore"] >= 2.5)
    is_burst = bool(features["is_burst"])
    predicted_fraud = bool(is_spike or is_velocity or is_anomaly or is_burst)
    fraud_score = (
        float(is_spike) * 0.35
        + float(is_velocity) * 0.25
        + float(is_anomaly) * 0.25
        + float(is_burst) * 0.15
    )
    return {
        "is_spike": is_spike,
        "is_velocity": is_velocity,
        "is_anomaly": is_anomaly,
        "predicted_fraud": predicted_fraud,
        "fraud_score": fraud_score,
    }
