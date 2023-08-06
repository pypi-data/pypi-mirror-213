import unittest
from capsphere.common.date import convert_date


class TestConvertDate(unittest.TestCase):

    date_format1 = '01Aug'
    date_format2 = '01/08/2022'
    date_format3 = '01/08'
    date_format4 = '010822'
    date_format5 = '101122'
    date_format6 = '01-08-2022'

    def test_convert_date(self):
        date1 = convert_date(self.date_format1, "2022")
        date2 = convert_date(self.date_format2)
        date3 = convert_date(self.date_format3, "2022")
        date4 = convert_date(self.date_format4)
        date5 = convert_date(self.date_format5)
        date6 = convert_date(self.date_format6)

        self.assertEqual(date1, 'Aug 2022')
        self.assertEqual(date2, 'Aug 2022')
        self.assertEqual(date3, 'Aug 2022')
        self.assertEqual(date4, 'Aug 2022')
        self.assertEqual(date5, 'Nov 2022')
        self.assertEqual(date6, 'Aug 2022')
