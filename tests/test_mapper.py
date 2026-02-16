import unittest
import pandas as pd
import os
from unittest.mock import patch
from src.mapper import map_data


class TestMapper(unittest.TestCase):

    def setUp(self):
        # Sample raw data
        self.raw_file = "test_raw.csv"
        raw_data = pd.DataFrame({
            "lookup_key": [1, 2, 2, 3]
        })
        raw_data.to_csv(self.raw_file, index=False)

        # Sample reference data
        self.ref_file = "test_reference.xlsx"
        ref_data = pd.DataFrame({
            "lookup_key": [1, 2, 3, 4],
            "name": ["A", "B", "C", "D"],
            "date_added": ["2024-01-01", "2024-02-01", "2024-03-01", "2024-04-01"]
        })
        ref_data.to_excel(self.ref_file, index=False)

    #  Successful mapping
    def test_mapping_success(self):
        summary = map_data(self.raw_file, self.ref_file, "test_output")

        self.assertEqual(summary["matched_records"], 3)
        self.assertEqual(summary["unmatched_records"], 0)
        self.assertTrue(os.path.exists(summary["matched_output_file"]))
        self.assertTrue(os.path.exists(summary["unmatched_output_file"]))

    # Unmatched scenario
    def test_unmatched_records(self):
        raw_data = pd.DataFrame({"lookup_key": [1, 99]})
        raw_data.to_csv(self.raw_file, index=False)

        summary = map_data(self.raw_file, self.ref_file, "test_output")

        self.assertEqual(summary["matched_records"], 1)
        self.assertEqual(summary["unmatched_records"], 1)

    # Empty raw file
    def test_empty_raw_file(self):
        pd.DataFrame(columns=["lookup_key"]).to_csv(self.raw_file, index=False)

        summary = map_data(self.raw_file, self.ref_file, "test_output")

        self.assertEqual(summary["total_raw_records"], 0)
        self.assertEqual(summary["matched_records"], 0)

    # Missing lookup column
    def test_missing_lookup_column(self):
        bad_ref = "bad_reference.xlsx"
        pd.DataFrame({"wrong_column": [1, 2, 3]}).to_excel(bad_ref, index=False)

        with self.assertRaises(ValueError):
            map_data(self.raw_file, bad_ref, "out")

        os.remove(bad_ref)

    #  PERFECT Mock Test
    @patch("src.mapper.os.path.exists")
    @patch("src.mapper.pd.read_excel")
    @patch("src.mapper.pd.read_csv")
    def test_mapping_with_mock(self, mock_csv, mock_excel, mock_exists):

        # Pretend files exist
        mock_exists.return_value = True

        mock_csv.return_value = pd.DataFrame({
            "lookup_key": [1, 2]
        })

        mock_excel.return_value = pd.DataFrame({
            "lookup_key": [1, 2],
            "name": ["A", "B"]
        })

        summary = map_data("fake_raw.csv", "fake_ref.xlsx", "test_output")

        self.assertEqual(summary["matched_records"], 2)
        self.assertEqual(summary["unmatched_records"], 0)

    # Cleanup
    def tearDown(self):
        for file in os.listdir():
            if file.startswith("test_") or file.startswith("unmatched_"):
                try:
                    os.remove(file)
                except:
                    pass


if __name__ == "__main__":
    unittest.main()
