import unittest
import pandas as pd
import os
from src.mapper import map_data


class TestMapper(unittest.TestCase):

    def setUp(self):
        # Create sample raw data
        self.raw_file = "test_raw.csv"
        raw_data = pd.DataFrame({"id": [1, 2, 2, 3]})
        raw_data.to_csv(self.raw_file, index=False)

        # Create sample reference data
        self.ref_file = "test_reference.xlsx"
        ref_data = pd.DataFrame({
            "lookup_key": [1, 2, 3, 4],
            "name": ["A", "B", "C", "D"]
        })
        ref_data.to_excel(self.ref_file, index=False)

        self.output_file = "test_output.csv"

    def test_mapping(self):
        result = map_data(self.raw_file, self.ref_file, self.output_file)

        # Check duplicates removed
        self.assertEqual(len(result), 3)

        # Check file created
        self.assertTrue(os.path.exists(self.output_file))

    def tearDown(self):
        # Clean up test files
        os.remove(self.raw_file)
        os.remove(self.ref_file)
        os.remove(self.output_file)


if __name__ == "__main__":
    unittest.main()
