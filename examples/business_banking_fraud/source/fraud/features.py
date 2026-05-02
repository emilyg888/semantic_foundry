from __future__ import annotations

from statistics import mean, pstdev


def build_features(amounts: list[float], amount: float, same_ts_count: int) -> dict[str, float | bool]:
    avg_amount = mean(amounts)
    std_amount = pstdev(amounts) or 1.0
    abs_amount = abs(amount)
    txn_count = len(amounts)
    z_score = (amount - avg_amount) / std_amount
    account_zscore = z_score
    is_burst = same_ts_count >= 3
    account_had_burst = is_burst or txn_count >= 12
    return {
        "abs_amount": abs_amount,
        "txn_count": txn_count,
        "same_ts_count": same_ts_count,
        "z_score": z_score,
        "account_zscore": account_zscore,
        "is_burst": is_burst,
        "account_had_burst": account_had_burst,
    }
