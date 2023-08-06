import os
import unittest

from capsphere.common.utils import get_test_resource_path
from capsphere.recognition.bank_statement.pdfplumber.reader import extract_bank_name
from io import BytesIO


class TestReader(unittest.TestCase):

    path_ambank = get_test_resource_path('ambank.pdf')
    path_ambank_2page = get_test_resource_path('test_ambank_2.pdf')
    path_cimb = get_test_resource_path('cimb.pdf')
    path_bad = get_test_resource_path('sotatek.pdf')

    def test_extract_names(self):
        ambank_output = extract_bank_name(self.path_ambank)
        ambank_2p_output = extract_bank_name(self.path_ambank_2page)
        cimb_output = extract_bank_name(self.path_cimb)
        self.assertEqual(ambank_output, 'AmBank')
        self.assertEqual(ambank_2p_output, 'AmBank')
        self.assertEqual(cimb_output, 'CIMB')

    def test_extract_name_bytesio(self):

        with open(self.path_ambank, "rb") as f:
            buf = BytesIO(f.read())
            output = extract_bank_name(buf)
            self.assertEqual(output, 'AmBank')

        with open(self.path_cimb, "rb") as f:
            buf = BytesIO(f.read())
            output = extract_bank_name(buf)
            self.assertEqual(output, 'CIMB')

    def test_extract_name_exception(self):
        folder_path = os.path.dirname(self.path_bad)
        file_path = os.path.join(folder_path, 'sotatek.pdf')
        with self.assertRaises(ValueError) as cm:
            extract_bank_name(self.path_bad)
        self.assertEqual(f"Unable to get bank name from {file_path}",
                         str(cm.exception))

    def test_extract_name_exception_bytesIO(self):
        with open(self.path_bad, "rb") as f:
            buf = BytesIO(f.read())
            with self.assertRaises(ValueError) as cm:
                extract_bank_name(buf)
            self.assertEqual(f"Unable to get bank name from {buf}",
                             str(cm.exception))
