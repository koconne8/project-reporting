import datetime

from holidays import GetHolidays, GetWorkingDays


def GetMonthlyExpected(month=datetime.datetime.now().month, year=datetime.datetime.now().year):
    # get the first and last day of the month
    first = datetime.date(year, month, 1)
    last = datetime.date(year, (month + 1), 1) - datetime.timedelta(days=1)

    # get our holidays
    holiday_list = GetHolidays(year)

    # setup a count for all weekdays
    # (Monday = [0], Tuesday = [1], etc...)
    weekdays = [0, 0, 0, 0, 0, 0, 0]

    # loop through from first to last day
    day = 1
    while day <= last.day:
        # get the new date
        next_day = datetime.date(year, month, day)
        # add one day to this week if it's not a paid holiday
        if next_day not in holiday_list:
            weekdays[next_day.weekday()] += 1
        day += 1

    # add up how many weekdays we have (Monday-Friday: [0]->[4])
    total = weekdays[0] + weekdays[1] + weekdays[2] + weekdays[3] + weekdays[4]

    return (total * 8)


def DateWorkingHours(day):
    if day.weekday() >= 5:
        return 0

    if day in GetHolidays(day.year):
        return 0

    return 8

def ManagerDateWorkingHours(day):
    if day.weekday() >= 5:
        return 0

    if day in GetHolidays(day.year):
        return 0

    working_days = GetWorkingDays(day.month, day.year)

    return float(30) / float(working_days)