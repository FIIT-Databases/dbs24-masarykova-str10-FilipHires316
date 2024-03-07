def date_formating(date):
    return date.isoformat().split('+')[0].rstrip('0') + date.isoformat()[26:29] if date is not None else None
