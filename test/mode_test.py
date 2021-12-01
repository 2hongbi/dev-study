import datetime
import pandas as pd
from datetime import date, timedelta


def test_date():
    cin_date = date(2021, 12, 22)
    days = timedelta(days=2)

    cout_date = cin_date + days

    print(cin_date.isoformat())
    print(cout_date.isoformat())

    t = '2021-12-25'
    cv_date = datetime.datetime.strptime(t, "%Y-%m-%d").date()
    print(cv_date)

    print(cv_date + days)


def test_cleansing():
    return
