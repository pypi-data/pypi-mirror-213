import unittest

from krxholidays import is_holiday_str


class TestHoliday(unittest.TestCase):

    def test_holiday_str(self):
        self.assertTrue(is_holiday_str("2021-01-01"), "신정")