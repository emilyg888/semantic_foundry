from __future__ import annotations

from semantic_foundry.config import UseCase


def build_semantic_sql(use_case: UseCase) -> str:
    return f"""-- Semantic_Foundry generated SQL
-- Use case: {use_case.use_case_id}
-- Target: {use_case.target}

create or replace view certified_customer as
select
  customer_id,
  customer_name,
  country,
  risk_rating
from customers;

create or replace view certified_account as
select
  account_id,
  customer_id,
  account_type,
  opened_date
from accounts;

create or replace view certified_merchant as
select distinct
  merchant_id,
  merchant_category,
  merchant_risk_rating
from transactions;

create or replace view certified_fraud_model_run as
select
  'baseline_rule_detector_run' as model_run_id,
  count(*) as evaluated_transaction_count,
  sum(case when fraud_flag = 1 then 1 else 0 end) as labelled_fraud_transaction_count
from transactions;

create or replace view certified_transaction as
select
  txn_id,
  account_id,
  merchant_id,
  merchant_category,
  merchant_risk_rating,
  txn_timestamp,
  amount,
  fraud_flag
from transactions;

create or replace view certified_fraud_signal as
select
  t.txn_id,
  t.account_id,
  abs(t.amount) as abs_amount,
  count(*) over (partition by t.account_id order by t.txn_timestamp rows between 9 preceding and current row) as txn_count,
  count(*) over (partition by t.account_id, t.txn_timestamp) as same_ts_count,
  case when count(*) over (partition by t.account_id, t.txn_timestamp) >= 3 then 1 else 0 end as is_burst,
  case when count(*) over (partition by t.account_id order by t.txn_timestamp rows between 9 preceding and current row) >= 10 then 1 else 0 end as account_had_burst,
  case when abs(t.amount) > 15000 or t.amount >= 3 * avg(t.amount) over (partition by t.account_id) then 1 else 0 end as z_score,
  case when abs(t.amount) > 15000 or t.amount >= 2.5 * avg(t.amount) over (partition by t.account_id) then 1 else 0 end as account_zscore,
  case when abs(t.amount) > 15000 then 1 else 0 end as is_spike,
  case when count(*) over (partition by t.account_id order by t.txn_timestamp rows between 9 preceding and current row) >= 10 then 1 else 0 end as is_velocity,
  case when abs(t.amount) > 15000 or t.amount >= 2.5 * avg(t.amount) over (partition by t.account_id) then 1 else 0 end as is_anomaly,
  case
    when abs(t.amount) > 15000
      or count(*) over (partition by t.account_id order by t.txn_timestamp rows between 9 preceding and current row) >= 10
      or abs(t.amount) > 15000 or t.amount >= 2.5 * avg(t.amount) over (partition by t.account_id)
      or count(*) over (partition by t.account_id, t.txn_timestamp) >= 3
    then 1 else 0
  end as predicted_fraud,
  (
    0.35 * case when abs(t.amount) > 15000 then 1 else 0 end
    + 0.25 * case when count(*) over (partition by t.account_id order by t.txn_timestamp rows between 9 preceding and current row) >= 10 then 1 else 0 end
    + 0.25 * case when abs(t.amount) > 15000 or t.amount >= 2.5 * avg(t.amount) over (partition by t.account_id) then 1 else 0 end
    + 0.15 * case when count(*) over (partition by t.account_id, t.txn_timestamp) >= 3 then 1 else 0 end
  ) as fraud_score
from transactions t;

create or replace view certified_fraud_alert as
select
  concat('alert_', txn_id) as alert_id,
  txn_id,
  account_id,
  predicted_fraud,
  fraud_score,
  is_spike,
  is_velocity,
  is_anomaly,
  case
    when is_velocity = 1 then 'Velocity burst'
    when is_spike = 1 then 'Amount spike'
    when is_anomaly = 1 then 'Statistical anomaly'
    else 'No alert'
  end as primary_alert_reason
from certified_fraud_signal
where predicted_fraud = 1;
"""
