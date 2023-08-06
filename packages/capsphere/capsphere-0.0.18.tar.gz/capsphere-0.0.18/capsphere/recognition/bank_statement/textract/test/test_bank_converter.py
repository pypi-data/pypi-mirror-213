import unittest
from capsphere.recognition.bank_statement.textract.converter import from_ambank
from decimal import Decimal


class TestBankConverter(unittest.TestCase):

    list_transaction = [
        {1: 'DATE', 2: 'TRANSACTION', 3: 'CHEQUE NO', 4: 'DEBIT', 5: 'CREDIT', 6: 'BALANCE'},
        {1: '', 2: 'BAL B/F ', 3: '', 4: '', 5: '', 6: '2,598.60'},
        {1: '1/08/2022', 2: 'TRANSFER TO ACC 1', 3: '', 4: '50.00', 5: '', 6: '2,548.60'},
        {1: '2/08/2022', 2: 'TRANSFER FROM A ', 3: '', 4: '', 5: '100.00', 6: '2,648.60'},
        {1: '1/08/2022', 2: 'TRANSFER TO ACC 2', 3: '', 4: '50.00', 5: '', 6: '2,598.60'},
        {1: '2/08/2022', 2: 'TRANSFER FROM B ', 3: '', 4: '', 5: '100.00', 6: '2,698.60'},
        {1: '2/08/2022', 2: 'TRANSFER FROM C ', 3: '', 4: '', 5: '100.00', 6: '2,798.60'},
        {1: '10/08/2022', 2: 'CHQ ', 3: '012345', 4: '1,200.10', 5: '', 6: '1,598.50 '}
    ]

    def test_func_ambank(self):
        output = from_ambank(self.list_transaction)
        start_balance, end_balance, total_debit, \
            total_credit, average_debit, average_credit, month = output
        self.assertEqual(start_balance, Decimal('2598.60'))
        self.assertEqual(end_balance, Decimal('1598.50'))
        self.assertEqual(total_debit, Decimal('1300.10'))
        self.assertEqual(total_credit, Decimal('300.00'))
        self.assertEqual(average_debit, Decimal('433.37'))
        self.assertEqual(average_credit, Decimal('100.00'))
        self.assertEqual(month, '10/08/2022')