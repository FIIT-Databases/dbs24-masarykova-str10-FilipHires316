def date_formating(date):
    return date.isoformat()[0:23] + date.isoformat()[26:29] if date is not None else None


def time_formating(time):
    time = str(time).rstrip('0')
    if time[-1] == '.':
        time += '0'
    time = time.split(':', 1)
    if len(time[0]) == 1:
        time[0] = time[0][:-2] + '0' + time[0][-1]
    elif time[0][-2] == ' ':
        time[0] = time[0][:-2] + ' 0' + time[0][-1]
    time = time[0] + ':' + time[1]
    return time
