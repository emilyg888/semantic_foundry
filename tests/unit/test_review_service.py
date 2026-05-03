from pathlib import Path
import shutil
import tempfile
import unittest

from semantic_foundry.config import BuildRequest
from semantic_foundry.review.service import add_issue, load_package_review_state, resolve_issue
from semantic_foundry.runtime import build


class ReviewServiceTests(unittest.TestCase):
    def test_load_package_review_state_populates_assets_and_gate(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            output_dir = build(
                BuildRequest(
                    source_path=Path("examples/business_banking_fraud/source"),
                    use_case_path=Path("examples/business_banking_fraud/use_case.yaml"),
                    output_root=Path(tmp_dir) / "outputs",
                    target="generic_sql",
                )
            )

            state = load_package_review_state(output_dir)

        self.assertGreater(len(state.review_assets), 0)
        self.assertEqual(state.gate.result, "not_certifiable")

    def test_add_and_resolve_issue_updates_issue_register(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            output_dir = build(
                BuildRequest(
                    source_path=Path("examples/business_banking_fraud/source"),
                    use_case_path=Path("examples/business_banking_fraud/use_case.yaml"),
                    output_root=Path(tmp_dir) / "outputs",
                    target="generic_sql",
                )
            )

            add_issue(
                package_path=output_dir,
                asset="certified_transaction",
                issue="Manual review required for transaction outliers.",
                severity="high",
                blocking=True,
                reported_by="QA",
            )
            resolve_issue(output_dir, "Manual review required for transaction outliers.", resolver="QA", resolution_note="Handled")
            state = load_package_review_state(output_dir)

        matching = [issue for issue in state.issues if issue["issue"] == "Manual review required for transaction outliers."]
        self.assertEqual(len(matching), 1)
        self.assertEqual(matching[0]["status"], "resolved")
        self.assertFalse(matching[0]["blocking"])


if __name__ == "__main__":
    unittest.main()
