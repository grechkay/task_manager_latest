from datetime import datetime, timedelta
from collections import Counter
from project_manager import ProjectManager
# import pandas as pd
import os
import pickle as pk

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    STRIKETHROUGH = '\033[07m'

class Ignore:
    def __init__(self):
        pm = ProjectManager()
        track_path = pm.personal_dir
        track_targets_path = '{}/track_targets'.format(track_path)
        self.ignore_path = "{}/__ignore__.pk".format(track_targets_path)
    def get_ignored_tracks(self):
        if os.path.exists(self.ignore_path):
            with open(self.ignore_path, 'rb') as f:
                ignored_tracks = pk.load(f)
        else:
            ignored_tracks = set()
        return ignored_tracks

def raise_fail_error(message):
    raise ValueError(bcolors.FAIL + "\n\n\t" + message + bcolors.ENDC + "\n")

def get_date_from_string(track_date):
    '''
    :param track_date: A string of a date in the form of YYYY-MM-DD or [t, y, tom] for today, yesterday tomorrow
    :return: The resulting string of date (useful if input was [t, y, tom] and a datetime date object
    '''
    if track_date == 't':  # today
        dt = datetime.now()
    elif track_date == 'y':  # yesterday
        dt = datetime.now() - timedelta(days=1)
    elif track_date == 'tom':  # tomorrow
        dt = datetime.now() + timedelta(days=1)
    else:
        try:
            dt = datetime.strptime(track_date, '%Y-%m-%d')
        except ValueError:
            raise_fail_error("Error. Date is not in the correct format YYYY-MM-DD (or [t, y, tom])")
    track_date = dt.strftime('%Y-%m-%d')  # this will get the good format so even if user types '2019-3-14' it still works
    dt = datetime.strptime(track_date, '%Y-%m-%d') # do this so that all days start at midnight, not RIGHT NOW (useful during tracking)
    return track_date, dt


def get_iso_info(mydate): # my date is a datetime object
    '''
    :param mydate: a datetime object
    :return: a dictionary with the following keys:
    -"year": int
    -"year_start": datetime object
    -"year_end": datetime ojbect
    -"quarter": int (between 1 and 4)
    -"quarter_start": datetime object
    -"quarter_end": datetime object
    -"month": int (between 1 and 12)
    -"month_start": datetime object
    -"month_end": datetime object
    -"week": int (between 1 and 53)
    -"week_start": datetime object
    -"week_end": datetime object
    -"day": int (between 1 and 7)

    Note: Called get_iso_info because the ISO calendar is EXACTLY what we are looking for.
    See here for more info: https://www.staff.science.uu.nl/~gent0113/calendar/isocalendar.htm
    '''
    # get iso calendar
    iso_year, iso_week, iso_day = mydate.isocalendar()

    '''
    CURRENT YEAR
    '''
    # already have current iso_week from above, just need the period

    # get the start date of current iso year
    year_start = datetime.strptime(str(iso_year) + ' 1 1', '%G %V %u')

    # get the end date of the current iso year
    next_year_start = datetime.strptime(str(iso_year + 1) + ' 1 1', '%G %V %u') # this is a monday
    year_end = next_year_start - timedelta(days=1) # this is a sunday


    '''
    CURRENT MONTH
    '''
    # like i said, the current month should be the majority of the current week
    month_of_week_days = [datetime.strptime(str(iso_year) + ' ' + str(iso_week) + ' ' + str(1 + i), '%G %V %u').month for i in range(7)]
    frequencies = list(Counter(month_of_week_days).items())
    iso_month = max(frequencies, key=lambda x: x[1])[0]

    # returns the start and end dates (both datetime objects) of an iso month
    # where the start date of the iso month must be a monday
    # and the end date of the iso month must be a sunday
    def get_period_of_iso_month(iso_year, iso_month):
        # 1. get the start of the current iso month
        # this is the week where the 4th of the current iso month is in.
        # this is because at "worst", 1 is a friday, 2 is a saturday, 3 is a sunday, and 4 is a monday --> ignore 1, 2, and 3 because they are not the majority of the week
        fourth_of_month = datetime(year=iso_year, month=iso_month, day=4)
        a, b, c = fourth_of_month.isocalendar() # a: year, b: week, c: day
        month_start = datetime.strptime(str(a) + ' ' + str(b) + ' ' + str(1), '%G %V %u') # brings us to the first day of this week

        # finally, get the iso end of the current iso month
        # first, get the last gregorian day of month
        temp = datetime(year=iso_year, month=iso_month, day=1) + timedelta(days=40) # temp is a day sometime in the next iso month (40 is arbitrary)
        next_month_start = datetime(year=temp.year, month=temp.month, day=1)
        this_month_end = next_month_start - timedelta(days=1)

        # get iso date of this
        this_month_end_iso = this_month_end.isocalendar()

        # if the day of the week of the last day is a thursday or LATER, then the last day of the month is the last day of this iso week
        # if the day of the week of the last day is a wednesday or EARLIER, then the last day of the month is the last day of the PREVIOUS iso week
        month_end = datetime.strptime(str(this_month_end_iso[0]) + ' ' + str(this_month_end_iso[1]) + ' ' + str(7), '%G %V %u') # potential month end unless last day is a wed. or earlier
        if this_month_end_iso[2] < 3:
            month_end = month_end - timedelta(weeks=1)
        return month_start, month_end

    month_start, month_end = get_period_of_iso_month(iso_year, iso_month)

    '''
    CURRENT QUARTER
    '''

    quarters = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]]


    iso_quarter = (iso_month - 1) // 3 + 1 # will be 1, 2, 3 or 4
    # now, get the START of the iso_quarter
    start_month_quarter = quarters[iso_quarter - 1][0]
    end_month_quarter = quarters[iso_quarter - 1][-1]

    quarter_start = get_period_of_iso_month(iso_year, start_month_quarter)[0]
    quarter_end = get_period_of_iso_month(iso_year, end_month_quarter)[1]


    '''
    CURRENT WEEK
    '''
    # already have the week number (iso week). just have to get the period

    # get the start date of current iso week
    week_start = datetime.strptime(str(iso_year) + ' ' + str(iso_week) + ' 1', '%G %V %u')

    # get the end date of the current iso week
    week_end = datetime.strptime(str(iso_year) + ' ' + str(iso_week) + ' 7', '%G %V %u')

    return {"year": iso_year, "year_start": year_start, "year_end": year_end,
            "quarter": iso_quarter, "quarter_start": quarter_start, "quarter_end": quarter_end,
            "month": iso_month, "month_start": month_start, "month_end": month_end,
            "week": iso_week, "week_start": week_start, "week_end": week_end,
            "day": iso_day}




def test_iso(Y, M, D):
    date = datetime(year=Y, month=M, day=D)
    result_dict = get_iso_info(date)
    print("date", date.date())
    print()
    print("current year:", result_dict["year"])
    print("year start:", result_dict["year_start"].date())
    print("year end:", result_dict["year_end"].date())
    print()
    print("current quarter:", result_dict["quarter"])
    print("quarter start:", result_dict["quarter_start"].date())
    print("quarter end:", result_dict["quarter_end"].date())
    print()
    print("current month:", result_dict["month"])
    print("month start:", result_dict["month_start"].date())
    print("month end:", result_dict["month_end"].date())
    print()
    print("current week:", result_dict["week"])
    print("week start:", result_dict["week_start"].date())
    print("week end:", result_dict["week_end"].date())
    print("----------------------------")


