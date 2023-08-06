__all__ = [
        'years',
        'days',
        'weeks',
        'months',
        'local_today',
        'local_now',
        'hours'
]

import datetime
import calendar

def years(start: datetime.date, end: datetime.date = None):
    end = end or datetime.date.today()
    leapdays = calendar.leapdays(start.year, end.year)
    diff = (end - start).days - leapdays
    return (diff/365).__round__(2)

def months(start: datetime.date, end: datetime.date = None):
    end = end or datetime.date.today()
    leapdays = calendar.leapdays(start.year, end.year)
    diff = (end - start).days - leapdays
    return (diff/30).__round__(1)

def days(start: datetime.date, end: datetime.date = None):
    end = end or datetime.date.today()
    return (end - start).days
    
def weeks(start: datetime.date, end: datetime.date = None):
    end = end or datetime.date.today()
    return ((end - start).days/7).__round__(1)

def local_now():
    return datetime.datetime.now(tz=datetime.timezone(offset=datetime.timedelta(hours=-3)))


def local_today():
    return local_now().date()


def hours(start: datetime.datetime, end: datetime.datetime = None):
    end = end or local_now()
    return ((end - start).days/24).__round__(1)