import datetime
import pandas as pd


def get_week_interval():
    today = datetime.datetime.now()
    todays_weekday = today.weekday()

    # check if end_date is a sunday
    # check if start_date is a monday
    end_date = today - datetime.timedelta(days=1 + todays_weekday)
    start_date = end_date - datetime.timedelta(days=6)

    return (start_date, end_date)


# get all the dates in between and store them in a list
def get_all_days_of_interval(start_date, end_date):
    return [pd.to_datetime(item) for item in pd.date_range(start_date, end_date)]


result = get_all_days_of_interval(*get_week_interval())
