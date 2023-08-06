import unittest
from capsphere.common.excel import create_worksheet
from openpyxl import load_workbook


class TestTextractExcel(unittest.TestCase):
    single_bank_output = [
        {'bank': 'Ambank', 'month': '31/08/2022', 'Total Debit': 400.00, 'Total Credit': 11900.00,
         'Average Debit': 100.00, 'Average Credit': 2380.00, \
         'Opening Balance': 3500.00, 'Closing Balance': 15000.00},
        {'bank': 'Ambank', 'month': '30/09/2022', 'Total Debit': 14500.00, 'Total Credit': 4500.00,
         'Average Debit': 7250.00, 'Average Credit': 1500.00, \
         'Opening Balance': 15000.00, 'Closing Balance': 5000.00},
    ]

    multiple_banks_output = [
        {'bank': 'Ambank', 'month': '31/08/2022', 'Total Debit': 400.00, 'Total Credit': 11900.00,
         'Average Debit': 100.00, 'Average Credit': 2380.00, \
         'Opening Balance': 3500.00, 'Closing Balance': 15000.00},
        {'bank': 'Ambank', 'month': '30/09/2022', 'Total Debit': 14500.00, 'Total Credit': 4500.00,
         'Average Debit': 7250.00, 'Average Credit': 1500.00, \
         'Opening Balance': 15000.00, 'Closing Balance': 5000.00},
        {'bank': 'Maybank', 'month': '28/01', 'Total Debit': 90000.90, 'Total Credit': 80000.50,
         'Average Debit': 45000.45, 'Average Credit': 40000.25, \
         'Opening Balance': 20000.00, 'Closing Balance': 9999.60},
    ]

    def test_create_worksheet_single_bank(self):
        file = create_worksheet(self.single_bank_output)

        workbook = load_workbook(file)
        sheet = workbook['Sheet1']
        self.assertEqual(sheet['A2'].value, 'Reconstructed Cash Flows')
        self.assertEqual(sheet['A3'].value, '*Average of 6 months bank statements')

        # Check first row (header)
        self.assertEqual(sheet['A5'].value, 'Ambank')
        self.assertEqual(sheet['B5'].value, 'Total Debit')
        self.assertEqual(sheet['C5'].value, 'Total Credit')
        self.assertEqual(sheet['D5'].value, 'Average Debit')
        self.assertEqual(sheet['E5'].value, 'Average Credit')
        self.assertEqual(sheet['F5'].value, 'Opening Balance')
        self.assertEqual(sheet['G5'].value, 'Closing Balance')

        # Check transaction row
        self.assertEqual(sheet['A6'].value, '31/08/2022')
        self.assertEqual(sheet['B6'].value, 400)
        self.assertEqual(sheet['C6'].value, 11900)
        self.assertEqual(sheet['D6'].value, 100)
        self.assertEqual(sheet['E6'].value, 2380)
        self.assertEqual(sheet['F6'].value, 3500)
        self.assertEqual(sheet['G6'].value, 15000)

        self.assertEqual(sheet['A7'].value, '30/09/2022')
        self.assertEqual(sheet['B7'].value, 14500)
        self.assertEqual(sheet['C7'].value, 4500)
        self.assertEqual(sheet['D7'].value, 7250)
        self.assertEqual(sheet['E7'].value, 1500)
        self.assertEqual(sheet['F7'].value, 15000)
        self.assertEqual(sheet['G7'].value, 5000)

        # Check total & average row
        self.assertEqual(sheet['A8'].value, 'Total')
        self.assertEqual(sheet['B8'].value, 14900)
        self.assertEqual(sheet['C8'].value, 16400)
        self.assertEqual(sheet['D8'].value, 7350)
        self.assertEqual(sheet['E8'].value, 3880)
        self.assertEqual(sheet['F8'].value, 18500)
        self.assertEqual(sheet['G8'].value, 20000)

        self.assertEqual(sheet['A9'].value, 'Average')
        self.assertEqual(sheet['B9'].value, 7450)
        self.assertEqual(sheet['C9'].value, 8200)
        self.assertEqual(sheet['D9'].value, 3675)
        self.assertEqual(sheet['E9'].value, 1940)
        self.assertEqual(sheet['F9'].value, 9250)
        self.assertEqual(sheet['G9'].value, 10000)

    def test_create_worksheet_multiple_banks(self):
        file = create_worksheet(self.multiple_banks_output)

        workbook = load_workbook(file)
        sheet = workbook['Sheet1']
        self.assertEqual(sheet['A2'].value, 'Reconstructed Cash Flows')
        self.assertEqual(sheet['A3'].value, '*Average of 6 months bank statements')

        # Check AMBANK first row (header)
        self.assertEqual(sheet['A5'].value, 'Ambank')
        self.assertEqual(sheet['B5'].value, 'Total Debit')
        self.assertEqual(sheet['C5'].value, 'Total Credit')
        self.assertEqual(sheet['D5'].value, 'Average Debit')
        self.assertEqual(sheet['E5'].value, 'Average Credit')
        self.assertEqual(sheet['F5'].value, 'Opening Balance')
        self.assertEqual(sheet['G5'].value, 'Closing Balance')

        self.assertEqual(sheet['A6'].value, '31/08/2022')
        self.assertEqual(sheet['B6'].value, 400)
        self.assertEqual(sheet['C6'].value, 11900)
        self.assertEqual(sheet['D6'].value, 100)
        self.assertEqual(sheet['E6'].value, 2380)
        self.assertEqual(sheet['F6'].value, 3500)
        self.assertEqual(sheet['G6'].value, 15000)

        self.assertEqual(sheet['A7'].value, '30/09/2022')
        self.assertEqual(sheet['B7'].value, 14500)
        self.assertEqual(sheet['C7'].value, 4500)
        self.assertEqual(sheet['D7'].value, 7250)
        self.assertEqual(sheet['E7'].value, 1500)
        self.assertEqual(sheet['F7'].value, 15000)
        self.assertEqual(sheet['G7'].value, 5000)

        self.assertEqual(sheet['A8'].value, 'Total')
        self.assertEqual(sheet['B8'].value, 14900)
        self.assertEqual(sheet['C8'].value, 16400)
        self.assertEqual(sheet['D8'].value, 7350)
        self.assertEqual(sheet['E8'].value, 3880)
        self.assertEqual(sheet['F8'].value, 18500)
        self.assertEqual(sheet['G8'].value, 20000)

        self.assertEqual(sheet['A9'].value, 'Average')
        self.assertEqual(sheet['B9'].value, 7450)
        self.assertEqual(sheet['C9'].value, 8200)
        self.assertEqual(sheet['D9'].value, 3675)
        self.assertEqual(sheet['E9'].value, 1940)
        self.assertEqual(sheet['F9'].value, 9250)
        self.assertEqual(sheet['G9'].value, 10000)

        # Check MAYBANK
        self.assertEqual(sheet['A12'].value, 'Maybank')
        self.assertEqual(sheet['B12'].value, 'Total Debit')
        self.assertEqual(sheet['C12'].value, 'Total Credit')
        self.assertEqual(sheet['D12'].value, 'Average Debit')
        self.assertEqual(sheet['E12'].value, 'Average Credit')
        self.assertEqual(sheet['F12'].value, 'Opening Balance')
        self.assertEqual(sheet['G12'].value, 'Closing Balance')

        self.assertEqual(sheet['A13'].value, '28/01')
        self.assertEqual(sheet['B13'].value, 90000.9)
        self.assertEqual(sheet['C13'].value, 80000.5)
        self.assertEqual(sheet['D13'].value, 45000.45)
        self.assertEqual(sheet['E13'].value, 40000.25)
        self.assertEqual(sheet['F13'].value, 20000)
        self.assertEqual(sheet['G13'].value, 9999.60)

        self.assertEqual(sheet['A14'].value, 'Total')
        self.assertEqual(sheet['B14'].value, 90000.9)
        self.assertEqual(sheet['C14'].value, 80000.5)
        self.assertEqual(sheet['D14'].value, 45000.45)
        self.assertEqual(sheet['E14'].value, 40000.25)
        self.assertEqual(sheet['F14'].value, 20000)
        self.assertEqual(sheet['G14'].value, 9999.60)

        self.assertEqual(sheet['A15'].value, 'Average')
        self.assertEqual(sheet['B15'].value, 90000.9)
        self.assertEqual(sheet['C15'].value, 80000.5)
        self.assertEqual(sheet['D15'].value, 45000.45)
        self.assertEqual(sheet['E15'].value, 40000.25)
        self.assertEqual(sheet['F15'].value, 20000)
        self.assertEqual(sheet['G15'].value, 9999.60)

        # Check overall table (Title, total row, average row)
        self.assertEqual(sheet['A18'].value, 'Reconstructed Cash Flow based on 6 months Bank Statements.')

        self.assertEqual(sheet['A24'].value, 'Total')
        self.assertEqual(sheet['B24'].value, 104900.9)
        self.assertEqual(sheet['C24'].value, 96400.5)
        self.assertEqual(sheet['D24'].value, 52350.45)
        self.assertEqual(sheet['E24'].value, 43880.25)
        self.assertEqual(sheet['F24'].value, 38500)
        self.assertEqual(sheet['G24'].value, 29999.6)

        self.assertEqual(sheet['A25'].value, 'Average')
        self.assertEqual(sheet['B25'].value, 34966.97)
        self.assertEqual(sheet['C25'].value, 32133.5)
        self.assertEqual(sheet['D25'].value, 17450.15)
        self.assertEqual(sheet['E25'].value, 14626.75)
        self.assertEqual(sheet['F25'].value, 12833.33)
        self.assertEqual(sheet['G25'].value, 9999.87)
