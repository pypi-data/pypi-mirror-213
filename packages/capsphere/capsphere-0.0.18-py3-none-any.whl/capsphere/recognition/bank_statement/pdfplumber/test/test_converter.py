import pdfplumber
import unittest

from capsphere.recognition.bank_statement.pdfplumber.converter import func_ambank, func_cimb, extract_date
from decimal import Decimal
from capsphere.common.utils import get_test_resource_path


class TestConverter(unittest.TestCase):

    path_ambank = get_test_resource_path('ambank.pdf')
    path_cimb = get_test_resource_path('cimb.pdf')
    path_cimb_2 = get_test_resource_path('cimb2.pdf')
    path_invalid = get_test_resource_path('sotatek.pdf')

    def test_func_ambank(self):
        output = func_ambank(self.path_ambank)
        start_balance, end_balance, total_debit, \
            total_credit, average_debit, average_credit, month = output
        self.assertEqual(start_balance, Decimal('83407.48'))
        self.assertEqual(end_balance, Decimal('49863.77'))
        self.assertEqual(total_debit, Decimal('227306.69'))
        self.assertEqual(total_credit, Decimal('193762.98'))
        self.assertEqual(average_debit, Decimal('1612.10'))
        self.assertEqual(average_credit, Decimal('9688.15'))
        self.assertEqual(month, 'Mar 2022')

    def test_func_cimb(self):
        output = func_cimb(self.path_cimb)
        start_balance, end_balance, total_debit, \
            total_credit, average_debit, average_credit, month = output
        self.assertEqual(start_balance, Decimal('686.21'))
        self.assertEqual(end_balance, Decimal('924.55'))
        self.assertEqual(total_debit, Decimal('34642.24'))
        self.assertEqual(total_credit, Decimal('34880.58'))
        self.assertEqual(average_debit, Decimal('314.93'))
        self.assertEqual(average_credit, Decimal('352.33'))
        self.assertEqual(month, 'Nov 2021')

    def test_func_cimb2(self):
        output = func_cimb(self.path_cimb_2)
        start_balance, end_balance, total_debit, \
            total_credit, average_debit, average_credit, month = output
        self.assertEqual(start_balance, Decimal('5306.37'))
        self.assertEqual(end_balance, Decimal('3972.36'))
        self.assertEqual(total_debit, Decimal('33727.81'))
        self.assertEqual(total_credit, Decimal('32393.80'))
        self.assertEqual(average_debit, Decimal('717.61'))
        self.assertEqual(average_credit, Decimal('469.48'))
        self.assertEqual(month, 'Oct 2022')

    def test_get_date(self):
        with pdfplumber.open(self.path_ambank) as pdf:
            self.assertEqual(extract_date(pdf.pages[0]), '31/03/2022')

        with pdfplumber.open(self.path_cimb) as pdf:
            self.assertEqual(extract_date(pdf.pages[0]), '07/12/2021')

        with pdfplumber.open(self.path_invalid) as pdf:
            self.assertEqual(extract_date(pdf.pages[0]), None)

