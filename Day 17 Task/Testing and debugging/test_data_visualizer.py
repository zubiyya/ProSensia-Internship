
import unittest
import pandas as pd

class TestSalesData(unittest.TestCase):
    def setUp(self):
        self.df = pd.read_csv("sales_data.csv")

    def test_columns_exist(self):
        self.assertIn("Product", self.df.columns)
        self.assertIn("Region", self.df.columns)
        self.assertIn("Sales", self.df.columns)

    def test_sales_positive(self):
        self.assertTrue((self.df["Sales"] > 0).all())

if __name__ == '__main__':
    unittest.main()
