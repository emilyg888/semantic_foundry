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
  case when abs(t.amount) > 15000 then 1 else 0 end as is_spike,
  case when count(*) over (partition by t.account_id order by t.txn_timestamp rows between 9 preceding and current row) >= 10 then 1 else 0 end as is_velocity
from transactions t;
"""
