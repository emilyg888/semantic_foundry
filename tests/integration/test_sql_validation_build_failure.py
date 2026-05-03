from pathlib import Path
import unittest
from unittest.mock import patch

from semantic_foundry.config import BuildRequest
from semantic_foundry.runtime import build
from semantic_foundry.validators.sql_validator import SqlValidationError


class SqlValidationBuildFailureIntegrationTests(unittest.TestCase):
    def test_build_fails_when_generated_sql_omits_required_view(self) -> None:
        with patch(
            "semantic_foundry.runtime.build_semantic_sql",
            return_value="create or replace view certified_customer as select customer_id, customer_name, country, risk_rating from customers;",
        ):
            with self.assertRaises(SqlValidationError) as context:
                build(
                    BuildRequest(
                        source_path=Path("examples/business_banking_fraud/source"),
                        use_case_path=Path("examples/business_banking_fraud/use_case.yaml"),
                        output_root=Path("outputs/sql_failure_runs"),
                        target="generic_sql",
                    )
                )

        self.assertIn("certified_account", str(context.exception))


if __name__ == "__main__":
    unittest.main()
