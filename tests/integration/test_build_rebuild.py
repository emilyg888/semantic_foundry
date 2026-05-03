from pathlib import Path
import unittest

from semantic_foundry.config import BuildRequest
from semantic_foundry.runtime import build


class BuildRebuildIntegrationTests(unittest.TestCase):
    def test_rebuild_cleans_stale_flat_output(self) -> None:
        output_root = Path("outputs/rebuild_runs")
        output_dir = output_root / "business_banking_fraud_detection"
        output_dir.mkdir(parents=True, exist_ok=True)
        stale_file = output_dir / "glossary.yaml"
        stale_file.write_text("stale\n", encoding="utf-8")

        built_dir = build(
            BuildRequest(
                source_path=Path("examples/business_banking_fraud/source"),
                use_case_path=Path("examples/business_banking_fraud/use_case.yaml"),
                output_root=output_root,
                target="generic_sql",
            )
        )

        self.assertEqual(built_dir, output_dir)
        self.assertFalse(stale_file.exists())
        self.assertTrue((built_dir / "01_semantic_catalogue" / "glossary.yaml").exists())
        self.assertTrue((built_dir / "07_delivery_pack" / "semantic_manifest.yaml").exists())


if __name__ == "__main__":
    unittest.main()
