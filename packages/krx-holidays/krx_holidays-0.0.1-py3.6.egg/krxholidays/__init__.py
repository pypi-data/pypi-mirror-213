from datetime import datetime
from krxholidays.data import holidays


def is_holiday_str(date_str: str, pattern: str = "%Y-%m-%d") -> bool:
    """
    주어진 날짜가 공휴일인지 확인합니다.
    """
    date = datetime.strptime(date_str, pattern)
    return is_holiday(date)


def is_holiday(date: datetime) -> bool:
    """
    주어진 날짜가 공휴일인지 확인합니다.
    """
    matched_list = list(filter(lambda x: x["day"] == date.strftime("%Y-%m-%d"), holidays))
    if len(matched_list) > 0:
        return True

    weekday = date.weekday()
    if weekday == 5 or weekday == 6:
        return True
    return False