from pathlib import Path
import tempfile
import unittest

from semantic_foundry.config import BuildRequest
from semantic_foundry.review.service import (
    approve_asset,
    load_package_review_state,
    publish_review_package,
    resolve_issue,
)
from semantic_foundry.runtime import build, certify


class ReviewPublishFlowIntegrationTests(unittest.TestCase):
    def test_review_activity_can_promote_package_to_candidate(self) -> None:
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
            for asset in state.review_assets:
                if asset.status != "candidate":
                    approve_asset(output_dir, asset.asset_type, asset.asset_id, reviewer="QA", comments="Approved in review cockpit test")

            resolve_issue(
                output_dir,
                "Synthetic fraud labels are suitable for accelerator validation only.",
                resolver="QA",
                resolution_note="Accepted for candidate package review.",
            )

            gate = publish_review_package(output_dir, publisher="QA", notes="Promoted candidate package")
            certify_payload = certify(output_dir)
            report = (output_dir / "07_delivery_pack" / "certification_report.md").read_text(encoding="utf-8")
            manifest = (output_dir / "07_delivery_pack" / "semantic_manifest.yaml").read_text(encoding="utf-8")
            approvals = (output_dir / "05_governance_controls" / "review_approvals.yaml").read_text(encoding="utf-8")
            publish_log = (output_dir / "07_delivery_pack" / "publish_log.yaml").read_text(encoding="utf-8")

        self.assertEqual(gate.result, "candidate")
        self.assertEqual(certify_payload["certification_result"], "candidate")
        self.assertIn("Result: `candidate`", report)
        self.assertIn('certification_status: "candidate"', manifest)
        self.assertIn("Approved in review cockpit test", approvals)
        self.assertIn("Promoted candidate package", publish_log)


if __name__ == "__main__":
    unittest.main()
