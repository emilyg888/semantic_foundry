from pathlib import Path
import shutil
import subprocess
import sys
import unittest


class CliSitTests(unittest.TestCase):
    def setUp(self) -> None:
        self.repo_root = Path.cwd()
        self.output_root = self.repo_root / "outputs" / "sit_runs"
        if self.output_root.exists():
            shutil.rmtree(self.output_root)

    def test_discover_build_and_certify_flow(self) -> None:
        discover = self.run_cli(
            "discover",
            "--source",
            "examples/business_banking_fraud/source",
            "--use-case",
            "examples/business_banking_fraud/use_case.yaml",
        )
        self.assertIn('"use_case_id": "business_banking_fraud_detection"', discover.stdout)
        self.assertIn('"python_functions"', discover.stdout)
        self.assertIn('"semantic_layer_candidates"', discover.stdout)
        self.assertIn('"signal_layer_candidates"', discover.stdout)
        self.assertIn('"alert_layer_candidates"', discover.stdout)
        self.assertIn('"business_customer"', discover.stdout)
        self.assertIn('"merchant"', discover.stdout)
        self.assertIn('"accepts"', discover.stdout)
        self.assertIn('"occurs_at"', discover.stdout)
        self.assertIn('"transacts_with"', discover.stdout)
        self.assertIn('"merchant_category"', discover.stdout)
        self.assertIn('"predicted_fraud"', discover.stdout)

        build = self.run_cli(
            "build",
            "--source",
            "examples/business_banking_fraud/source",
            "--use-case",
            "examples/business_banking_fraud/use_case.yaml",
            "--target",
            "generic_sql",
            "--output-root",
            str(self.output_root),
        )
        output_dir = Path(build.stdout.strip())
        self.assertTrue(output_dir.exists())
        self.assertTrue((output_dir / "README.md").exists())
        self.assertTrue((output_dir / "01_semantic_catalogue" / "glossary.yaml").exists())
        self.assertTrue((output_dir / "03_prediction_catalogue" / "predictions.yaml").exists())
        self.assertTrue((output_dir / "04_evaluation_metric_catalogue" / "metrics.yaml").exists())
        self.assertTrue((output_dir / "05_governance_controls" / "dq_validation.yaml").exists())
        self.assertTrue((output_dir / "05_governance_controls" / "policy_validation.yaml").exists())

        certify = self.run_cli("certify", "--package", str(output_dir))
        self.assertIn('"certification_report_present": true', certify.stdout)
        self.assertIn('"semantic_manifest_present": true', certify.stdout)
        self.assertIn('"certification_result": "not_certifiable"', certify.stdout)
        self.assertIn('"validation_status": "passed"', certify.stdout)

    def run_cli(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, "main.py", *args],
            cwd=self.repo_root,
            check=True,
            capture_output=True,
            text=True,
        )


if __name__ == "__main__":
    unittest.main()
