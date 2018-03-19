from analyzer.LieDetector import LieDetector
from datetime import date

a = LieDetector()

assert -1 == a.check_month_day(40, 2)
assert 0 == a.check_month_day(28, 2)
assert a.has_numbers('long2string') is True
assert a.has_numbers('name') is False
assert 21 == a.calculate_age(date(1996, 3, 7))
assert 17 == a.calculate_age(date(1999, 10, 14))
assert 'Monday' == a.weekday(0)
assert 'Sunday' == a.weekday(6)
assert 'December' == a.months(12)
assert 'June' == a.months(6)
assert ('Are you Ula?', 1) == a.complete_question(
    "Are you <name>?", ["Ula", "02-07-1996"])
assert ('Were you born in 1995?', 0) == a.complete_question(
    "Were you born in <tyear>?", ["Ula", "02-07-1996"])
