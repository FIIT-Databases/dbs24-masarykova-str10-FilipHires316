import datetime


def date_formating(date):
    return date.isoformat()[0:23] + date.isoformat()[26:29] if date is not None else None


def time_formating(time):
    time = str(time).rstrip('0')
    if time[-1] == '.':
        time += '0'
    if time[1] == ':':
        time = '0' + time
    return time
