from pathlib import Path
import unittest

from semantic_foundry.builders.manifest_builder import build_semantic_manifest
from semantic_foundry.intake.intake_loader import load_use_case
from semantic_foundry.package.publisher import expected_generated_assets
from semantic_foundry.scanners.source_inventory import build_source_inventory


class ManifestBuilderTests(unittest.TestCase):
    def test_manifest_includes_nested_generated_assets_and_inventory_counts(self) -> None:
        source_path = Path("examples/business_banking_fraud/source")
        use_case_path = Path("examples/business_banking_fraud/use_case.yaml")
        use_case = load_use_case(use_case_path)
        inventory = build_source_inventory(source_path)

        manifest = build_semantic_manifest(
            use_case=use_case,
            inventory=inventory,
            generated_assets=expected_generated_assets(),
            source_path=source_path,
            use_case_path=use_case_path,
            validation_status="passed",
            certification_status="candidate",
        )

        self.assertIn("run", manifest)
        self.assertEqual(manifest["run"]["generated_assets"], expected_generated_assets())
        self.assertEqual(manifest["run"]["inventory_counts"]["python"], 2)
        self.assertEqual(manifest["run"]["generation_mode"], "build")
        self.assertEqual(manifest["run"]["validation_status"], "passed")
        self.assertEqual(manifest["run"]["certification_status"], "candidate")


if __name__ == "__main__":
    unittest.main()
