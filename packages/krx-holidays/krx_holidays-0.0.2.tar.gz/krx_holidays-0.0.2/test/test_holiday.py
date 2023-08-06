import unittest
from datetime import datetime

from krxholidays import is_holiday_str, get_day_info, is_holiday


class TestHoliday(unittest.TestCase):

    def test_holiday_str(self):
        self.assertTrue(is_holiday_str("2021-01-01"), "신정")
        self.assertTrue(is_holiday_str("2021-01-02"), "주말")
        self.assertTrue(is_holiday_str("2021-01-03"), "주말")
        self.assertFalse(is_holiday_str("2021-01-04"), "평일")

    def test_holiday_datetime(self):
        self.assertTrue(is_holiday(datetime(2021, 1, 1)), "신정")
        self.assertTrue(is_holiday(datetime(2021, 1, 2)), "주말")
        self.assertTrue(is_holiday(datetime(2021, 1, 3)), "주말")
        self.assertFalse(is_holiday(datetime(2021, 1, 4)), "평일")

    def test_holiday_info(self):
        dinfo = get_day_info(datetime(2021, 1, 1))
        self.assertEqual(dinfo["desc"], "신정")
        self.assertEqual(dinfo["week_name"], "금요일")
        self.assertTrue(dinfo["is_holiday"])

        dinfo = get_day_info(datetime(2021, 1, 2))
        self.assertEqual(dinfo["desc"], "주말")
        self.assertEqual(dinfo["week_name"], "토요일")
        self.assertTrue(dinfo["is_holiday"])

        dinfo = get_day_info(datetime(2021, 1, 3))
        self.assertEqual(dinfo["desc"], "주말")
        self.assertEqual(dinfo["week_name"], "일요일")
        self.assertTrue(dinfo["is_holiday"])

        dinfo = get_day_info(datetime(2021, 1, 4))
        self.assertEqual(dinfo["desc"], "평일")
        self.assertEqual(dinfo["week_name"], "월요일")
        self.assertFalse(dinfo["is_holiday"])