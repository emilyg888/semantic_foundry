from pathlib import Path
import unittest

from semantic_foundry.builders.package_index_builder import build_package_index
from semantic_foundry.intake.intake_loader import load_use_case


class PackageIndexBuilderTests(unittest.TestCase):
    def test_build_package_index_lists_review_sections(self) -> None:
        use_case = load_use_case(Path("examples/business_banking_fraud/use_case.yaml"))

        package_index = build_package_index(use_case)

        self.assertIn("Semantic_Foundry Package Index", package_index)
        self.assertIn(use_case.use_case_id, package_index)
        self.assertIn("01_semantic_catalogue/", package_index)
        self.assertIn("03_prediction_catalogue/", package_index)
        self.assertIn("04_evaluation_metric_catalogue/", package_index)
        self.assertIn("dq_validation.yaml", package_index)
        self.assertIn("07_delivery_pack/", package_index)


if __name__ == "__main__":
    unittest.main()
