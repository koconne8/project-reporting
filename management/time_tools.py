import datetime

from holidays import get_holidays, get_working_days


def get_monthly_expected(month=datetime.datetime.now().month, year=datetime.datetime.now().year):
    # get the first and last day of the month
    last = datetime.date(year, (month + 1), 1) - datetime.timedelta(days=1)

    # get our holidays
    holiday_list = get_holidays(year)

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

    return total * 8


def date_working_hours(day):
    if day.weekday() >= 5:
        return 0

    if day in get_holidays(day.year):
        return 0

    return 8


def manager_date_working_hours(day):
    if day.weekday() >= 5:
        return 0

    if day in get_holidays(day.year):
        return 0

    working_days = get_working_days(day.month, day.year)

    return float(30) / float(working_days)
