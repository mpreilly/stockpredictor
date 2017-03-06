from yahoo_finance import Share
import csv
from datetime import date
from datetime import timedelta

stocks = ['AMD', 'MU', 'BKS']
start_date = date(2016, 3, 3)
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
        share.refresh()     # Refresh data from yahoo_finance
        history = share.get_historical(start_date.isoformat(), end_date.isoformat())
        numDays = len(history)
        row = (stock, ) + get_prices(history)
        writer.writerow(row)
    writer.writerow("")

with open('stocks.csv', 'rt') as csvfile:
    reader = csv.reader(csvfile)
    changeRows = []

    for row in reader:
        if len(row) < 1:
            break
        if row[0] != '':
            changeRow = (row[0], '', )
            for i in range(2, numDays+1):
                changeRow += (100 * ((float(row[i]) - float(row[i-1])) / float(row[i-1])),)
            changeRows.append(changeRow)

with open('stocks.csv', 'a') as csvfile:
    writer = csv.writer(csvfile)
    for row in changeRows:
        writer.writerow(row)
