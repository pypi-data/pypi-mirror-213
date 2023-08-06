import unittest
import pandas as pd

from capsphere.common.utils import flatten_list, get_file_format, process_text, read_config, sort_rows_by_month
from capsphere.resources.test.data import FILE_NAME_1, FILE_NAME_2, FILE_NAME_3, BALANCE, ORDER_1, ORDER_2, ORDER_3, \
    ORDER_4, ORDER_5, ORDER_6


class TestUtils(unittest.TestCase):

    banks = ["AmBank", "CIMB", "Maybank",
             "Maybank Islamic", "Alliance", "Hong Leong",
             "RHB", "RHB Islamic", "Public Bank"]

    def test_valid_file_split(self):
        pdf_file = get_file_format(FILE_NAME_1)
        img_file = get_file_format(FILE_NAME_2)
        self.assertEqual(pdf_file, 'pdf')
        self.assertEqual(img_file, 'img')

    def test_invalid_file_split(self):
        with self.assertRaises(ValueError) as cm:
            get_file_format(FILE_NAME_3)
        self.assertEqual("Unrecognised filename format 'invalid.file.extension': "
                         "Unable to split strings",
                         str(cm.exception))

    def test_decimal_encoder(self):
        # TODO add resources here
        pass

    def test_process_text(self):
        headers_ambank = process_text(["date", "transaction", "cheque no.", "debit", "credit", "balance"])
        headers_cimb = process_text(["date", "description", "cheque / ref no", "withdrawal", "deposits", "balance"])

        self.assertEqual(headers_ambank, ["date", "transaction", "cheque_no", "debit", "credit", "balance"])
        self.assertEqual(headers_cimb, ["date", "description", "cheque_ref_no", "withdrawal", "deposits", "balance"])

    def test_flatten_list(self):
        data = [["date", "transaction", "cheque no.", "debit", "credit", "balance"]]
        expected = ["date", "transaction", "cheque no.", "debit", "credit", "balance"]
        actual = flatten_list(data)
        self.assertEqual(len(actual),  6)
        self.assertEqual(actual, expected)

    def test_row_order(self):
        df_1 = pd.DataFrame(BALANCE, index=ORDER_1)
        df_2 = pd.DataFrame(BALANCE, index=ORDER_2)
        df_3 = pd.DataFrame(BALANCE, index=ORDER_3)
        df_4 = pd.DataFrame(BALANCE, index=ORDER_4)
        df_5 = pd.DataFrame(BALANCE, index=ORDER_5)
        df_6 = pd.DataFrame(BALANCE, index=ORDER_6)

        output_1 = sort_rows_by_month(df_1)
        output_2 = sort_rows_by_month(df_2)
        output_3 = sort_rows_by_month(df_3)
        output_4 = sort_rows_by_month(df_4)
        output_5 = sort_rows_by_month(df_5)
        output_6 = sort_rows_by_month(df_6)

        self.assertEqual(output_1.index.values.tolist(), ['Aug 2022', 'Sep 2022'])
        self.assertEqual(output_2.index.values.tolist(), ['Aug 2022', 'Sep 2022'])
        self.assertEqual(output_3.index.values.tolist(), ['Aug 2022', 'Aug 2022'])
        self.assertEqual(output_4.index.values.tolist(), ['Aug 2021', 'Aug 2022'])
        self.assertEqual(output_5.index.values.tolist(), ['Sep 2021', 'Aug 2022'])
        self.assertEqual(output_6.index.values.tolist(), ['Aug 2022', 'Sep 2023'])