def date_formating(date):
    return date.isoformat()[0:23] + date.isoformat()[26:29] if date is not None else None
