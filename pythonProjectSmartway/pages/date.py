import datetime
from datetime import timedelta

def date_flight(number):
    today = datetime.datetime.now()
    date = datetime.datetime.strftime(today + timedelta(days=number), "%d.%m.%Y")
    print(date)
    return date

