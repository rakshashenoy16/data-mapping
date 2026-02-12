import unittest
import pandas as pd
import os
from src.mapper import map_data


class TestMapper(unittest.TestCase):

    def setUp(self):
        # Create sample raw data
        self.raw_file = "test_raw.csv"
        raw_data = pd.DataFrame({
            "lookup_key": [1, 2, 2, 3]
        })
        raw_data.to_csv(self.raw_file, index=False)

        # Create sample reference data
        self.ref_file = "test_reference.xlsx"
        ref_data = pd.DataFrame({
            "lookup_key": [1, 2, 3, 4],
            "name": ["A", "B", "C", "D"],
            "date_added": ["2024-01-01", "2024-02-01", "2024-03-01", "2024-04-01"]
        })
        ref_data.to_excel(self.ref_file, index=False)

    def test_mapping_success(self):
        summary = map_data(self.raw_file, self.ref_file, "test_output")

        self.assertEqual(summary["matched_records"], 3)
        self.assertEqual(summary["unmatched_records"], 0)
        self.assertTrue(os.path.exists(summary["matched_output_file"]))
        self.assertTrue(os.path.exists(summary["unmatched_output_file"]))

    def test_missing_lookup_column(self):
        bad_ref = "bad_reference.xlsx"
        pd.DataFrame({"wrong_column": [1, 2, 3]}).to_excel(bad_ref, index=False)

        with self.assertRaises(ValueError):
            map_data(self.raw_file, bad_ref, "out")

        os.remove(bad_ref)

    def tearDown(self):
        for file in os.listdir():
            if file.startswith("test_") or file.startswith("unmatched_"):
                try:
                    os.remove(file)
                except:
                    pass


if __name__ == "__main__":
    unittest.main()
