from pathlib import Path
import unittest

from semantic_foundry.scanners.source_inventory import build_source_inventory


class SourceInventoryTests(unittest.TestCase):
    def test_inventory_classifies_python_sources(self) -> None:
        root = Path("examples/business_banking_fraud/source")
        inventory = build_source_inventory(root)

        categories = inventory.counts_by_category
        self.assertEqual(categories["python"], 2)
        self.assertIn("fraud/features.py", [item.path for item in inventory.files])


if __name__ == "__main__":
    unittest.main()
