from yahoo_finance import Share
import csv
from datetime import date
from datetime import timedelta

stocks = ['AMD', 'MU', 'SQ', 'AAPL', 'NVDA', 'BKS']
start_date = date(2017, 2, 6)
end_date = date.today()

def is_market_open(curdate):
    closed_dates = [date(2017, 1, 2),
                    date(2017, 1, 16),
                    date(2017, 2, 20),
                    date(2017, 4, 14),
                    date(2017, 5, 29),
                    date(2017, 7, 4),
                    date(2017, 9, 4),
                    date(2017, 11, 23),
                    date(2017, 12, 25)]
    if curdate.weekday() > 4:
        return False
    for closed in closed_dates:
        if curdate == closed:
            return False
    return True

def get_prices(history):
    prices = ()
    while len(history) != 0:
        info = history.pop()
        prices += (info.get('Close'),)
    return prices

def get_dates():
    dates = ()
    curdate = start_date
    while curdate <= end_date:
        if is_market_open(curdate):
            dates += (curdate.isoformat(), )
        curdate += timedelta(days=1)
    return dates


with open('stocks.csv', 'wb') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(('',) + get_dates())
    for stock in stocks:
        share = Share(stock)
        history = share.get_historical(start_date.isoformat(), end_date.isoformat())
        row = (stock, ) + get_prices(history)
        writer.writerow(row)
