from pathlib import Path
import unittest

from semantic_foundry.scanners.python_logic_miner import mine_python_logic


class PythonLogicMinerTests(unittest.TestCase):
    def test_mines_feature_and_detector_functions(self) -> None:
        root = Path("examples/business_banking_fraud/source")
        functions = mine_python_logic(root)
        function_names = {function.function_name for function in functions}

        self.assertIn("build_features", function_names)
        self.assertIn("predict_fraud", function_names)

        feature_function = next(function for function in functions if function.function_name == "build_features")
        self.assertIn("abs_amount", feature_function.assigned_names)
        self.assertIn("txn_count", feature_function.assigned_names)


if __name__ == "__main__":
    unittest.main()
